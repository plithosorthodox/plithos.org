#!/usr/bin/env python3
"""Export one privacy-safe monthly Cloudflare Web Analytics snapshot.

The exporter requests aggregate datasets only and writes a whitelisted summary.
It never downloads or stores raw request or beacon events.
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple


GRAPHQL_URL = "https://api.cloudflare.com/client/v4/graphql"
HOST = "plithos.org"
SMALL_BUCKET_THRESHOLD = 20
LOCALES = {
    "en", "el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it",
    "sr", "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur",
    "bg",
}
PUBLIC_PAGES = {
    "calendar", "saints", "churches", "library", "reader", "prayers", "rule",
    "glossary", "contact", "embed",
}
LIMITS = {
    "daily": 40,
    "paths": 1000,
    "countries": 250,
    "devices": 20,
    "referrers": 250,
    "browsers": 100,
    "operatingSystems": 100,
}


TRAFFIC_QUERY = r"""
query MonthlyTraffic($accountTag: string!, $siteTag: string!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: {accountTag: $accountTag}) {
      totals: rumPageloadEventsAdaptiveGroups(
        limit: 1
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } avg { sampleInterval } }
      daily: rumPageloadEventsAdaptiveGroups(
        limit: 40
        orderBy: [date_ASC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { date } }
      paths: rumPageloadEventsAdaptiveGroups(
        limit: 1000
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { requestPath } }
      countries: rumPageloadEventsAdaptiveGroups(
        limit: 250
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { countryName } }
      devices: rumPageloadEventsAdaptiveGroups(
        limit: 20
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { deviceType } }
      referrers: rumPageloadEventsAdaptiveGroups(
        limit: 250
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { refererHost } }
    }
  }
}
"""


CLIENT_QUERY = r"""
query MonthlyClients($accountTag: string!, $siteTag: string!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: {accountTag: $accountTag}) {
      browsers: rumPageloadEventsAdaptiveGroups(
        limit: 100
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { userAgentBrowser } }
      operatingSystems: rumPageloadEventsAdaptiveGroups(
        limit: 100
        orderBy: [count_DESC]
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { count sum { visits } dimensions { userAgentOS } }
    }
  }
}
"""


VITALS_QUERY = r"""
query MonthlyVitals($accountTag: string!, $siteTag: string!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: {accountTag: $accountTag}) {
      vitals: rumWebVitalsEventsAdaptiveGroups(
        limit: 1
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) {
        count
        avg { sampleInterval }
        quantiles {
          cumulativeLayoutShiftP75
          firstContentfulPaintP75
          interactionToNextPaintP75
          largestContentfulPaintP75
          timeToFirstByteP75
        }
        sum {
          visits
          clsGood clsNeedsImprovement clsPoor clsTotal
          inpGood inpNeedsImprovement inpPoor inpTotal
          lcpGood lcpNeedsImprovement lcpPoor lcpTotal
          ttfbGood ttfbNeedsImprovement ttfbPoor ttfbTotal
        }
      }
    }
  }
}
"""


FCP_QUERY = r"""
query MonthlyFcp($accountTag: string!, $siteTag: string!, $start: Date!, $end: Date!) {
  viewer {
    accounts(filter: {accountTag: $accountTag}) {
      vitals: rumWebVitalsEventsAdaptiveGroups(
        limit: 1
        filter: {siteTag: $siteTag, requestHost: "plithos.org", bot: 0, date_geq: $start, date_lt: $end}
      ) { sum { fcpGood fcpNeedsImprovement fcpPoor fcpTotal } }
    }
  }
}
"""


class SnapshotError(RuntimeError):
    """The analytics response cannot produce a safe complete snapshot."""


def month_bounds(month: str) -> Tuple[dt.date, dt.date]:
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        raise SnapshotError("month must use YYYY-MM")
    year, number = (int(part) for part in month.split("-"))
    if number < 1 or number > 12:
        raise SnapshotError("month must use YYYY-MM")
    start = dt.date(year, number, 1)
    if number == 12:
        end = dt.date(year + 1, 1, 1)
    else:
        end = dt.date(year, number + 1, 1)
    return start, end


def previous_month(today: Optional[dt.date] = None) -> str:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    first = today.replace(day=1)
    prior = first - dt.timedelta(days=1)
    return prior.strftime("%Y-%m")


def ensure_completed_month(month: str, today: Optional[dt.date] = None) -> Tuple[dt.date, dt.date]:
    start, end = month_bounds(month)
    today = today or dt.datetime.now(dt.timezone.utc).date()
    if end > today.replace(day=1):
        raise SnapshotError("the requested month is current or future")
    return start, end


def graphql(token: str, query: str, variables: Mapping[str, str]) -> Mapping[str, Any]:
    body = json.dumps({"query": query, "variables": dict(variables)}).encode("utf-8")
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "plithos-monthly-analytics/1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SnapshotError("Cloudflare GraphQL returned HTTP %d" % exc.code) from None
    except urllib.error.URLError as exc:
        raise SnapshotError("Cloudflare GraphQL request failed: %s" % exc.reason) from None
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise SnapshotError("Cloudflare GraphQL returned invalid JSON") from None
    if not isinstance(result, dict):
        raise SnapshotError("Cloudflare GraphQL returned an invalid response")
    errors = result.get("errors")
    if errors:
        messages = []
        for error in errors:
            if isinstance(error, dict) and isinstance(error.get("message"), str):
                messages.append(error["message"])
        raise SnapshotError("Cloudflare GraphQL error: " + "; ".join(messages or ["unknown error"]))
    return result


def account_data(response: Mapping[str, Any]) -> Mapping[str, Any]:
    try:
        accounts = response["data"]["viewer"]["accounts"]
    except (KeyError, TypeError):
        raise SnapshotError("Cloudflare response has no account data") from None
    if not isinstance(accounts, list) or len(accounts) != 1 or not isinstance(accounts[0], dict):
        raise SnapshotError("Cloudflare response did not contain exactly one account result")
    return accounts[0]


def number(value: Any, label: str, integer: bool = True) -> Any:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SnapshotError("%s is not numeric" % label)
    if value < 0:
        raise SnapshotError("%s is negative" % label)
    if integer:
        if int(value) != value:
            raise SnapshotError("%s is not an integer count" % label)
        return int(value)
    return float(value)


def row_counts(row: Mapping[str, Any], label: str) -> Tuple[int, int]:
    count = number(row.get("count"), label + ".count")
    sums = row.get("sum")
    if not isinstance(sums, dict):
        raise SnapshotError(label + ".sum is missing")
    visits = number(sums.get("visits"), label + ".visits")
    return count, visits


def dimension(row: Mapping[str, Any], field: str, label: str) -> str:
    dimensions = row.get("dimensions")
    if not isinstance(dimensions, dict) or not isinstance(dimensions.get(field), str):
        raise SnapshotError("%s.%s is missing" % (label, field))
    return dimensions[field]


def assert_not_truncated(data: Mapping[str, Any]) -> None:
    for name, limit in LIMITS.items():
        rows = data.get(name)
        if not isinstance(rows, list):
            raise SnapshotError("%s result is missing" % name)
        if len(rows) >= limit:
            raise SnapshotError("%s reached its row limit and may be truncated" % name)


def normalize_public_path(path: str) -> Tuple[str, Optional[str]]:
    if not isinstance(path, str) or not path.startswith("/"):
        return "other_or_invalid", None
    if "?" in path or "#" in path or "\\" in path or "\x00" in path:
        return "other_or_invalid", None
    compact = re.sub(r"/+", "/", path)
    if compact != "/":
        compact = compact.rstrip("/")
    parts = [part for part in compact.split("/") if part]
    if not parts:
        return "/", None
    if len(parts) == 1 and parts[0] in PUBLIC_PAGES:
        return "/" + parts[0], None
    locale = parts[0]
    if locale not in LOCALES:
        return "other_or_invalid", None
    if len(parts) == 1:
        return "/" + locale, locale
    if len(parts) == 2 and parts[1] in PUBLIC_PAGES:
        return "/" + locale + "/" + parts[1], locale
    return "other_or_invalid", None


def sorted_rows(rows: Iterable[Mapping[str, Any]], name_field: str) -> List[Dict[str, Any]]:
    return sorted(
        (dict(row) for row in rows),
        key=lambda row: (-int(row["pageviews_estimated"]), str(row[name_field]).lower()),
    )


def aggregate_named(
    rows: Sequence[Mapping[str, Any]],
    dimension_field: str,
    output_field: str,
    label: str,
    threshold: Optional[int] = None,
    empty_label: Optional[str] = None,
    other_label: str = "other",
) -> List[Dict[str, Any]]:
    seen = set()
    values: MutableMapping[str, List[int]] = {}
    for index, row in enumerate(rows):
        raw = dimension(row, dimension_field, "%s[%d]" % (label, index))
        if raw in seen:
            raise SnapshotError("%s contains a duplicate dimension" % label)
        seen.add(raw)
        name = empty_label if raw == "" and empty_label else raw
        count, visits = row_counts(row, "%s[%d]" % (label, index))
        bucket = values.setdefault(name, [0, 0])
        bucket[0] += count
        bucket[1] += visits
    other = [0, 0]
    published = []
    for name, counts in values.items():
        if threshold is not None and counts[0] < threshold:
            other[0] += counts[0]
            other[1] += counts[1]
        else:
            published.append({
                output_field: name,
                "pageviews_estimated": counts[0],
                "visits_estimated": counts[1],
            })
    if other[0] and (threshold is None or other[0] >= threshold):
        published.append({
            output_field: other_label,
            "pageviews_estimated": other[0],
            "visits_estimated": other[1],
        })
    return sorted_rows(published, output_field)


def aggregate_referrers(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    published = []
    suppressed_external = False
    for index, row in enumerate(rows):
        raw = dimension(row, "refererHost", "referrers[%d]" % index)
        if raw in seen:
            raise SnapshotError("referrers contains a duplicate dimension")
        seen.add(raw)
        count, visits = row_counts(row, "referrers[%d]" % index)
        if count < SMALL_BUCKET_THRESHOLD:
            if raw:
                suppressed_external = True
            continue
        published.append({
            "host": raw or "direct_or_unavailable",
            "pageviews_estimated": count,
            "visits_estimated": visits,
        })
    published = sorted_rows(published, "host")
    if suppressed_external:
        published.append({
            "host": "other_external",
            "pageviews_suppressed_below": SMALL_BUCKET_THRESHOLD,
            "visits_suppressed_below": SMALL_BUCKET_THRESHOLD,
        })
    return published


def build_daily(rows: Sequence[Mapping[str, Any]], start: dt.date, end: dt.date) -> List[Dict[str, Any]]:
    by_date: Dict[str, Tuple[int, int]] = {}
    for index, row in enumerate(rows):
        day = dimension(row, "date", "daily[%d]" % index)
        try:
            parsed = dt.date.fromisoformat(day)
        except ValueError:
            raise SnapshotError("daily result has an invalid date") from None
        if not start <= parsed < end:
            raise SnapshotError("daily result is outside the requested month")
        if day in by_date:
            raise SnapshotError("daily result contains a duplicate date")
        by_date[day] = row_counts(row, "daily[%d]" % index)
    output = []
    current = start
    while current < end:
        day = current.isoformat()
        count, visits = by_date.get(day, (0, 0))
        output.append({"date": day, "pageviews_estimated": count, "visits_estimated": visits})
        current += dt.timedelta(days=1)
    return output


def build_routes(rows: Sequence[Mapping[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    routes: MutableMapping[str, List[int]] = {}
    locales: MutableMapping[str, int] = {}
    seen = set()
    for index, row in enumerate(rows):
        raw = dimension(row, "requestPath", "paths[%d]" % index)
        if raw in seen:
            raise SnapshotError("paths contains a duplicate dimension")
        seen.add(raw)
        path, locale = normalize_public_path(raw)
        count, visits = row_counts(row, "paths[%d]" % index)
        bucket = routes.setdefault(path, [0, 0])
        bucket[0] += count
        bucket[1] += visits
        if locale:
            locales[locale] = locales.get(locale, 0) + count
    route_rows = [
        {"path": path, "pageviews_estimated": values[0], "visits_estimated": values[1]}
        for path, values in routes.items()
    ]
    route_rows = sorted_rows(route_rows, "path")
    locale_rows = []
    for locale, count in locales.items():
        locale_rows.append({"locale": locale, "pageviews_estimated": count})
    locale_rows.sort(key=lambda row: (-int(row["pageviews_estimated"]), row["locale"]))
    return route_rows, locale_rows


def rating_counts(sums: Mapping[str, Any], prefix: str, label: str) -> Dict[str, int]:
    return {
        "good": number(sums.get(prefix + "Good"), label + ".good"),
        "needs_improvement": number(sums.get(prefix + "NeedsImprovement"), label + ".needs_improvement"),
        "poor": number(sums.get(prefix + "Poor"), label + ".poor"),
        "total": number(sums.get(prefix + "Total"), label + ".total"),
    }


def milliseconds(value: Any, label: str) -> float:
    microseconds = number(value, label, integer=False)
    return round(microseconds / 1000.0, 3)


def build_vitals(main: Mapping[str, Any], fcp: Mapping[str, Any]) -> Dict[str, Any]:
    main_rows = main.get("vitals")
    fcp_rows = fcp.get("vitals")
    if not isinstance(main_rows, list) or len(main_rows) != 1:
        raise SnapshotError("vitals result is missing or ambiguous")
    if not isinstance(fcp_rows, list) or len(fcp_rows) != 1:
        raise SnapshotError("FCP result is missing or ambiguous")
    row = main_rows[0]
    fcp_row = fcp_rows[0]
    if not isinstance(row, dict) or not isinstance(fcp_row, dict):
        raise SnapshotError("vitals result is invalid")
    quantiles = row.get("quantiles")
    sums = row.get("sum")
    fcp_sums = fcp_row.get("sum")
    average = row.get("avg")
    if not all(isinstance(item, dict) for item in (quantiles, sums, fcp_sums, average)):
        raise SnapshotError("vitals aggregates are missing")
    return {
        "events_estimated": number(row.get("count"), "vitals.count"),
        "visits_estimated": number(sums.get("visits"), "vitals.visits"),
        "p75": {
            "cumulative_layout_shift": number(quantiles.get("cumulativeLayoutShiftP75"), "vitals.clsP75", integer=False),
            "first_contentful_paint_ms": milliseconds(quantiles.get("firstContentfulPaintP75"), "vitals.fcpP75"),
            "interaction_to_next_paint_ms": milliseconds(quantiles.get("interactionToNextPaintP75"), "vitals.inpP75"),
            "largest_contentful_paint_ms": milliseconds(quantiles.get("largestContentfulPaintP75"), "vitals.lcpP75"),
            "time_to_first_byte_ms": milliseconds(quantiles.get("timeToFirstByteP75"), "vitals.ttfbP75"),
        },
        "quality_counts_estimated": {
            "cumulative_layout_shift": rating_counts(sums, "cls", "vitals.cls"),
            "first_contentful_paint": rating_counts(fcp_sums, "fcp", "vitals.fcp"),
            "interaction_to_next_paint": rating_counts(sums, "inp", "vitals.inp"),
            "largest_contentful_paint": rating_counts(sums, "lcp", "vitals.lcp"),
            "time_to_first_byte": rating_counts(sums, "ttfb", "vitals.ttfb"),
        },
    }


def confidence_95(estimate: int, sample_interval: float) -> Dict[str, Any]:
    if sample_interval <= 1:
        return {
            "lower": float(estimate),
            "upper": float(estimate),
            "sample_size": estimate,
            "valid": False,
        }
    sample_size = int(round(estimate / sample_interval))
    probability = 1.0 / sample_interval
    standard_error = math.sqrt(sample_size * (1.0 - probability)) * sample_interval
    margin = 1.96 * standard_error
    return {
        "lower": round(max(0.0, estimate - margin), 2),
        "upper": round(estimate + margin, 2),
        "sample_size": sample_size,
        "valid": False,
    }


def build_snapshot(
    month: str,
    captured_at: str,
    release_build: Optional[str],
    traffic: Mapping[str, Any],
    clients: Mapping[str, Any],
    vitals: Mapping[str, Any],
    fcp: Mapping[str, Any],
    correction_reason: Optional[str] = None,
) -> Dict[str, Any]:
    start, end = month_bounds(month)
    traffic_data = account_data(traffic)
    client_data = account_data(clients)
    vitals_data = account_data(vitals)
    fcp_data = account_data(fcp)
    combined = dict(traffic_data)
    combined.update(client_data)
    assert_not_truncated(combined)
    totals = traffic_data.get("totals")
    if not isinstance(totals, list) or len(totals) != 1 or not isinstance(totals[0], dict):
        raise SnapshotError("totals result is missing or ambiguous")
    pageviews, visits = row_counts(totals[0], "totals")
    average = totals[0].get("avg")
    if not isinstance(average, dict):
        raise SnapshotError("totals sample interval is missing")
    sample_interval = number(average.get("sampleInterval"), "totals.sampleInterval", integer=False)
    routes, locale_paths = build_routes(traffic_data["paths"])
    snapshot: Dict[str, Any] = {
        "schema_version": 1,
        "site": HOST,
        "period": {
            "month": month,
            "start_utc": start.isoformat() + "T00:00:00Z",
            "end_utc_exclusive": end.isoformat() + "T00:00:00Z",
        },
        "collected_at_utc": captured_at,
        "source": {
            "provider": "Cloudflare Web Analytics",
            "pageview_dataset": "rumPageloadEventsAdaptiveGroups",
            "vitals_dataset": "rumWebVitalsEventsAdaptiveGroups",
            "request_host": HOST,
            "bot_filter": 0,
            "adaptive_sampling": True,
            "average_sample_interval": sample_interval,
            "counts_are_estimates": True,
        },
        "release": {"build": release_build, "source_commit": None},
        "totals": {
            "pageviews_estimated": pageviews,
            "visits_estimated": visits,
            "confidence_95": {
                "pageviews": confidence_95(pageviews, sample_interval),
                "visits": confidence_95(visits, sample_interval),
            },
        },
        "daily": build_daily(traffic_data["daily"], start, end),
        "routes": routes,
        "explicit_locale_paths": locale_paths,
        "devices": aggregate_named(traffic_data["devices"], "deviceType", "device", "devices"),
        "browsers": aggregate_named(client_data["browsers"], "userAgentBrowser", "browser", "browsers", SMALL_BUCKET_THRESHOLD),
        "operating_systems": aggregate_named(client_data["operatingSystems"], "userAgentOS", "operating_system", "operatingSystems", SMALL_BUCKET_THRESHOLD),
        "countries": aggregate_named(traffic_data["countries"], "countryName", "country", "countries", SMALL_BUCKET_THRESHOLD),
        "referrers": aggregate_referrers(traffic_data["referrers"]),
        "core_web_vitals": build_vitals(vitals_data, fcp_data),
        "privacy": {
            "raw_events_stored": False,
            "small_bucket_threshold": SMALL_BUCKET_THRESHOLD,
            "cross_dimension_tables": False,
            "excluded": [
                "ip_addresses",
                "visitor_and_session_identifiers",
                "full_user_agents_and_versions",
                "query_strings",
                "free_text_searches",
                "exact_event_timestamps",
                "referrer_paths",
            ],
        },
        "limitations": [
            "Counts are adaptive-sampling estimates and are rounded in increments of the sample interval.",
            "The reported 95 percent confidence intervals are marked invalid because Cloudflare does not validate this approximation.",
            "A zero visit value in a subgroup does not prove that no visit occurred.",
            "Visits are not unique people.",
            "Explicit locale paths are a lower bound on language use.",
            "Referrer data does not include query strings or campaign parameters.",
        ],
    }
    if correction_reason:
        snapshot["correction"] = {"reason": correction_reason}
    validate_snapshot(snapshot)
    return snapshot


def validate_snapshot(snapshot: Mapping[str, Any]) -> None:
    allowed = {
        "schema_version", "site", "period", "collected_at_utc", "source", "release",
        "privacy", "totals", "daily", "routes", "explicit_locale_paths", "devices",
        "browsers", "operating_systems", "countries", "referrers",
        "core_web_vitals", "limitations", "correction",
    }
    unexpected = set(snapshot) - allowed
    if unexpected:
        raise SnapshotError("snapshot contains unapproved fields: " + ", ".join(sorted(unexpected)))
    rendered = json.dumps(snapshot, ensure_ascii=False).lower()
    forbidden = ("authorization", "bearer ", "account_id", "accounttag", "sitetag")
    for word in forbidden:
        if word in rendered:
            raise SnapshotError("snapshot contains a forbidden identifier field")


def percent(part: int, whole: int) -> str:
    if not whole:
        return "0%"
    return "%d%%" % round(100 * part / whole)


def markdown(snapshot: Mapping[str, Any]) -> str:
    month = str(snapshot["period"]["month"])
    start = dt.date.fromisoformat(month + "-01")
    title = "%s %d" % (calendar.month_name[start.month], start.year)
    totals = snapshot["totals"]
    pageviews = int(totals["pageviews_estimated"])
    visits = int(totals["visits_estimated"])
    devices = {row["device"]: row for row in snapshot["devices"]}
    mobile = int(devices.get("mobile", {}).get("pageviews_estimated", 0))
    lines = [
        "# Plithos traffic - " + title,
        "",
        "Cloudflare Web Analytics aggregate for the completed UTC month. Known bots",
        "and non-production hosts are excluded. Counts are adaptive-sampling estimates,",
        "not exact visitor records.",
        "",
        "## Summary",
        "",
        "- Estimated pageviews: %s" % format(pageviews, ","),
        "- Estimated visits: %s" % format(visits, ","),
        "- Mobile pageviews: %s (%s)" % (format(mobile, ","), percent(mobile, pageviews)),
        "- Average sample interval: %s" % snapshot["source"]["average_sample_interval"],
        "",
        "## Routes",
        "",
        "| route | estimated pageviews | share |",
        "|---|---:|---:|",
    ]
    for row in snapshot["routes"][:12]:
        lines.append("| `%s` | %s | %s |" % (
            row["path"], format(int(row["pageviews_estimated"]), ","),
            percent(int(row["pageviews_estimated"]), pageviews),
        ))
    p75 = snapshot["core_web_vitals"]["p75"]
    lines.extend([
        "",
        "## Field performance",
        "",
        "| metric | P75 |",
        "|---|---:|",
        "| Largest Contentful Paint | %s ms |" % p75["largest_contentful_paint_ms"],
        "| Interaction to Next Paint | %s ms |" % p75["interaction_to_next_paint_ms"],
        "| Cumulative Layout Shift | %s |" % p75["cumulative_layout_shift"],
        "| First Contentful Paint | %s ms |" % p75["first_contentful_paint_ms"],
        "| Time to First Byte | %s ms |" % p75["time_to_first_byte_ms"],
        "",
        "## Privacy and limitations",
        "",
        "Only aggregate rows are kept. No raw requests, IP addresses, identifiers,",
        "full user agents, query strings, search terms, exact event times or referrer",
        "paths are stored. Buckets below %d estimated pageviews are combined where" % SMALL_BUCKET_THRESHOLD,
        "they could describe readers rather than public site routes.",
        "",
    ])
    for item in snapshot["limitations"]:
        lines.append("- " + str(item))
    if snapshot.get("correction"):
        lines.extend(["", "## Correction", "", str(snapshot["correction"]["reason"])])
    lines.append("")
    return "\n".join(lines)


def live_build() -> Optional[str]:
    request = urllib.request.Request(
        "https://plithos.org/version.json",
        headers={"User-Agent": "plithos-monthly-analytics/1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    build = payload.get("build") if isinstance(payload, dict) else None
    return build if isinstance(build, str) and len(build) <= 80 else None


def write_snapshot(snapshot: Mapping[str, Any], output_dir: Path, replace: bool) -> Tuple[Path, Path]:
    month = str(snapshot["period"]["month"])
    json_path = output_dir / (month + ".json")
    md_path = output_dir / (month + ".md")
    if not replace:
        if json_path.exists() and md_path.exists():
            return json_path, md_path
        if json_path.exists() or md_path.exists():
            raise SnapshotError("the monthly snapshot is incomplete; use an explicit correction")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    json_path.write_text(json_text, encoding="utf-8", newline="\n")
    md_path.write_text(markdown(snapshot), encoding="utf-8", newline="\n")
    return json_path, md_path


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", help="completed UTC month in YYYY-MM form")
    parser.add_argument("--output-dir", default="analytics/traffic", type=Path)
    parser.add_argument("--replace", action="store_true", help="replace an existing snapshot")
    parser.add_argument("--correction-reason", help="required reason recorded when replacing")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    month = args.month or previous_month()
    try:
        start, end = ensure_completed_month(month)
        if args.replace != bool(args.correction_reason):
            raise SnapshotError("--replace and --correction-reason must be used together")
        json_path = args.output_dir / (month + ".json")
        md_path = args.output_dir / (month + ".md")
        if not args.replace and json_path.exists() and md_path.exists():
            print("Monthly traffic snapshot already exists for " + month)
            return 0
        token = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN", "")
        account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
        site_tag = os.environ.get("CLOUDFLARE_WEB_ANALYTICS_SITE_TAG", "")
        if not token or not account_id or not site_tag:
            raise SnapshotError(
                "CLOUDFLARE_ANALYTICS_TOKEN, CLOUDFLARE_ACCOUNT_ID and "
                "CLOUDFLARE_WEB_ANALYTICS_SITE_TAG are required"
            )
        variables = {
            "accountTag": account_id,
            "siteTag": site_tag,
            "start": start.isoformat(),
            "end": end.isoformat(),
        }
        traffic = graphql(token, TRAFFIC_QUERY, variables)
        clients = graphql(token, CLIENT_QUERY, variables)
        vitals = graphql(token, VITALS_QUERY, variables)
        fcp = graphql(token, FCP_QUERY, variables)
        captured = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        snapshot = build_snapshot(
            month, captured, live_build(), traffic, clients, vitals, fcp,
            correction_reason=args.correction_reason,
        )
        written = write_snapshot(snapshot, args.output_dir, args.replace)
        print("Wrote " + " and ".join(str(path) for path in written))
        return 0
    except SnapshotError as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
