import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "traffic_snapshot", ROOT / "tools" / "export_traffic_snapshot.py"
)
traffic = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(traffic)


def envelope(account):
    return {"data": {"viewer": {"accounts": [account]}}, "errors": None}


def row(count, visits, field=None, value=None):
    result = {"count": count, "sum": {"visits": visits}}
    if field is not None:
        result["dimensions"] = {field: value}
    return result


class TrafficSnapshotTests(unittest.TestCase):
    def responses(self):
        traffic_response = envelope({
            "totals": [{"count": 100, "sum": {"visits": 40}, "avg": {"sampleInterval": 10}}],
            "daily": [row(100, 40, "date", "2026-10-01")],
            "paths": [
                row(60, 20, "requestPath", "/"),
                row(20, 10, "requestPath", "/es/prayers"),
                row(20, 10, "requestPath", "/private-text@example.com"),
            ],
            "countries": [
                row(80, 30, "countryName", "US"),
                row(10, 10, "countryName", "DE"),
                row(10, 0, "countryName", "FR"),
            ],
            "devices": [row(70, 20, "deviceType", "mobile"), row(30, 20, "deviceType", "desktop")],
            "referrers": [
                row(80, 30, "refererHost", ""),
                row(10, 10, "refererHost", "example.com"),
                row(10, 0, "refererHost", "other.example"),
            ],
        })
        clients_response = envelope({
            "browsers": [row(80, 30, "userAgentBrowser", "Chrome"), row(10, 10, "userAgentBrowser", "RareBrowser"), row(10, 0, "userAgentBrowser", "OtherRare")],
            "operatingSystems": [row(80, 30, "userAgentOS", "Android"), row(20, 10, "userAgentOS", "iOS")],
        })
        vital_sum = {
            "visits": 40,
            "clsGood": 90, "clsNeedsImprovement": 0, "clsPoor": 10, "clsTotal": 100,
            "inpGood": 100, "inpNeedsImprovement": 0, "inpPoor": 0, "inpTotal": 100,
            "lcpGood": 90, "lcpNeedsImprovement": 10, "lcpPoor": 0, "lcpTotal": 100,
            "ttfbGood": 80, "ttfbNeedsImprovement": 20, "ttfbPoor": 0, "ttfbTotal": 100,
        }
        vitals_response = envelope({"vitals": [{
            "count": 100,
            "avg": {"sampleInterval": 10},
            "quantiles": {
                "cumulativeLayoutShiftP75": 0.01,
                "firstContentfulPaintP75": 700000,
                "interactionToNextPaintP75": 80000,
                "largestContentfulPaintP75": 900000,
                "timeToFirstByteP75": 300000,
            },
            "sum": vital_sum,
        }]})
        fcp_response = envelope({"vitals": [{"sum": {
            "fcpGood": 90, "fcpNeedsImprovement": 10, "fcpPoor": 0, "fcpTotal": 100,
        }}]})
        return traffic_response, clients_response, vitals_response, fcp_response

    def test_month_validation(self):
        self.assertEqual(traffic.previous_month(dt.date(2026, 11, 13)), "2026-10")
        with self.assertRaises(traffic.SnapshotError):
            traffic.ensure_completed_month("2026-11", dt.date(2026, 11, 13))

    def test_every_query_has_the_production_privacy_filters(self):
        for query in (
            traffic.TRAFFIC_QUERY,
            traffic.CLIENT_QUERY,
            traffic.VITALS_QUERY,
            traffic.FCP_QUERY,
        ):
            compact = " ".join(query.split())
            self.assertIn('requestHost: "plithos.org"', compact)
            self.assertIn("bot: 0", compact)
            self.assertIn("siteTag: $siteTag", compact)
            self.assertIn("date_geq: $start", compact)
            self.assertIn("date_lt: $end", compact)

    def test_confidence_shape_matches_schema(self):
        self.assertEqual(
            traffic.confidence_95(490, 10),
            {"lower": 359.84, "upper": 620.16, "sample_size": 49, "valid": False},
        )
        self.assertEqual(
            traffic.confidence_95(140, 10),
            {"lower": 70.43, "upper": 209.57, "sample_size": 14, "valid": False},
        )

    def test_snapshot_suppresses_unknown_paths_and_small_reader_buckets(self):
        snapshot = traffic.build_snapshot(
            "2026-10", "2026-11-13T00:00:00Z", "2026-10-07b",
            *self.responses(),
        )
        paths = {item["path"]: item["pageviews_estimated"] for item in snapshot["routes"]}
        self.assertEqual(paths["other_or_invalid"], 20)
        self.assertNotIn("private-text@example.com", json.dumps(snapshot))
        countries = {item["country"]: item["pageviews_estimated"] for item in snapshot["countries"]}
        self.assertEqual(countries, {"US": 80, "other": 20})
        referrers = {item["host"]: item for item in snapshot["referrers"]}
        self.assertEqual(referrers["direct_or_unavailable"]["pageviews_estimated"], 80)
        self.assertEqual(referrers["other_external"]["pageviews_suppressed_below"], 20)
        self.assertEqual(snapshot["core_web_vitals"]["p75"]["largest_contentful_paint_ms"], 900.0)
        self.assertFalse(snapshot["totals"]["confidence_95"]["pageviews"]["valid"])

    def test_markdown_and_write_are_deterministic_and_idempotent(self):
        snapshot = traffic.build_snapshot(
            "2026-10", "2026-11-13T00:00:00Z", "2026-10-07b",
            *self.responses(),
        )
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            json_path, md_path = traffic.write_snapshot(snapshot, output, False)
            first_json = json_path.read_text(encoding="utf-8")
            first_md = md_path.read_text(encoding="utf-8")
            traffic.write_snapshot(snapshot, output, False)
            self.assertEqual(first_json, json_path.read_text(encoding="utf-8"))
            self.assertEqual(first_md, md_path.read_text(encoding="utf-8"))
            self.assertIn("P75", first_md)


if __name__ == "__main__":
    unittest.main()
