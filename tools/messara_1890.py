#!/usr/bin/env python3
"""Audit and stage the 1890 Messara Arabic Chrysostom Liturgy.

The source is a complete 1890 Beirut printed edition. The working scan is an
OrthodoxOnline upload on Scribd. The underlying 1890 text is public domain,
but the access scan is labeled BY-NC. This helper never writes scan images into
the repository and never treats OCR as source text.

The public-domain text is transcribed as a separate historical edition. It is
not used to fill gaps in the 1628 Balamand manuscript.

Examples:

    PYTHONUTF8=1 python tools/messara_1890.py --check
    PYTHONUTF8=1 python tools/messara_1890.py --verify-images C:/path/to/pages
    PYTHONUTF8=1 python tools/messara_1890.py --print-map
    PYTHONUTF8=1 python tools/messara_1890.py --write-staging

The final library writer is deliberately gated by two independent visual
reconciliations, zero unresolved readings, exact page continuity, and explicit
reviewer kinds and methods. It does not update the works index or any served
page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPTS = ROOT / "tools" / "manuscripts"
MANIFEST = MANUSCRIPTS / "messara_1890_chrysostom.json"
RANGE_SPECS = (
    (50, 67, MANUSCRIPTS / "messara_1890_chrysostom_pages_50_67_transcription.json"),
    (68, 85, MANUSCRIPTS / "messara_1890_chrysostom_pages_68_85_transcription.json"),
)
STAGING = MANUSCRIPTS / "messara_1890_chrysostom_library_staging.json"
FINAL = ROOT / "data" / "library" / "divine-liturgy-chrysostom-ar-messara-1890.json"
ASSET_BASE = "https://html.scribdassets.com/79y9wu4vls2xkpps/images"
FORBIDDEN_DASHES = ("\u2013", "\u2014")
ALLOWED_ROLES = {
    "heading", "rubric", "prayer", "deacon", "choir", "response",
    "body", "footnote",
}
ALLOWED_REGIONS = {
    "full-width", "right-column", "left-column", "bottom-footnote",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def default_image_dir() -> Path:
    override = os.environ.get("PLITHOS_MESSARA_1890_IMAGES")
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / "plithos-arabic-messara-1890" / "pages"


def image_map(manifest: dict) -> dict[int, dict]:
    return {
        int(page["scan_page"]): page
        for page in manifest["working_images"]["pages"]
    }


def asset_url(page: dict) -> str:
    return "%s/%s.jpg" % (ASSET_BASE, page["asset_id"])


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    raw = MANIFEST.read_text(encoding="utf-8")
    if any(mark in raw for mark in FORBIDDEN_DASHES):
        errors.append("manifest contains an en dash or em dash")

    source = manifest.get("source", {})
    if source.get("publication_year") != 1890:
        errors.append("source publication year is not 1890")
    if source.get("access_document_id") != "173168212":
        errors.append("source document identifier changed")
    rights = source.get("rights", {})
    if "Public domain" not in rights.get("underlying_text", ""):
        errors.append("underlying text rights are not recorded")
    if "BY-NC" not in rights.get("access_scan", ""):
        errors.append("access scan license is not recorded")

    scope = manifest.get("scope", {})
    if scope.get("start", {}).get("scan_page") != 50:
        errors.append("Chrysostom start page is not 50")
    if scope.get("end", {}).get("scan_page") != 85:
        errors.append("Chrysostom end page is not 85")
    if scope.get("preceding_page", {}).get("scan_page") != 49:
        errors.append("preceding portrait page is not 49")
    if scope.get("following_page", {}).get("scan_page") != 86:
        errors.append("following Basil portrait page is not 86")
    if scope.get("page_count") != 36:
        errors.append("source range page count is not 36")

    images = manifest.get("working_images", {})
    pages = images.get("pages", [])
    numbers = [page.get("scan_page") for page in pages]
    if numbers != list(range(50, 86)):
        errors.append("working image map must contain scan pages 50 through 85 once")
    if sum(int(page.get("bytes", 0)) for page in pages) != images.get("total_bytes"):
        errors.append("working image total byte count is stale")
    names = [page.get("filename") for page in pages]
    if len(names) != len(set(names)):
        errors.append("working image filenames are not unique")
    hashes = [page.get("sha256") for page in pages]
    if len(hashes) != len(set(hashes)):
        errors.append("working image hashes are not unique")
    for page in pages:
        number = page.get("scan_page")
        asset_id = page.get("asset_id", "")
        expected_prefix = "%s-" % number
        if not asset_id.startswith(expected_prefix):
            errors.append("scan page %s has a mismatched asset id" % number)
        expected_name = "page-%03d__%s.jpg" % (number, asset_id.split("-", 1)[1])
        if page.get("filename") != expected_name:
            errors.append("scan page %s has a mismatched working filename" % number)
        if len(page.get("sha256", "")) != 64:
            errors.append("scan page %s has an invalid SHA-256" % number)

    review = manifest.get("review", {})
    human_review = review.get("qualified_human_arabic_review", {})
    if human_review.get("completed"):
        if not human_review.get("reviewer") or not human_review.get("method"):
            errors.append("completed human review lacks reviewer or method")
    if review.get("publication_ready"):
        for field in (
            "continuous_transcription",
            "page_continuity_checked",
            "zero_unresolved_readings",
            "two_independent_visual_reconciliations",
        ):
            if review.get(field) is not True:
                errors.append("manifest claims readiness without %s" % field)
    return errors


def verify_images(directory: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    for page in manifest["working_images"]["pages"]:
        path = directory / page["filename"]
        number = page["scan_page"]
        if not path.is_file():
            errors.append("scan page %s image is missing: %s" % (number, path))
            continue
        size = path.stat().st_size
        if size != page["bytes"]:
            errors.append(
                "scan page %s image is %d bytes, expected %d"
                % (number, size, page["bytes"])
            )
        actual = digest(path)
        if actual.lower() != page["sha256"].lower():
            errors.append(
                "scan page %s SHA-256 is %s, expected %s"
                % (number, actual, page["sha256"])
            )
    return errors


def validate_range(
    path: Path, start: int, end: int, manifest: dict
) -> tuple[list[str], dict | None]:
    errors: list[str] = []
    if not path.is_file():
        return errors, None
    raw = path.read_text(encoding="utf-8")
    if any(mark in raw for mark in FORBIDDEN_DASHES):
        errors.append("%s contains an en dash or em dash" % path.name)
    try:
        data = json.loads(raw)
    except ValueError as exc:
        return ["%s is not valid JSON: %s" % (path.name, exc)], None

    if data.get("source_manifest") != "tools/manuscripts/%s" % MANIFEST.name:
        errors.append("%s has the wrong source manifest" % path.name)
    scope = data.get("scope", {})
    expected_pages = list(range(start, end + 1))
    if scope.get("scan_pages") != expected_pages:
        errors.append("%s scope must list scan pages %d through %d" % (path.name, start, end))
    if scope.get("page_count") != len(expected_pages):
        errors.append("%s page count is not %d" % (path.name, len(expected_pages)))

    pages = data.get("pages", [])
    if [page.get("scan_page") for page in pages] != expected_pages:
        errors.append("%s page records are not scan pages %d through %d" % (path.name, start, end))
    images = image_map(manifest)
    block_ids: set[str] = set()
    for page in pages:
        number = page.get("scan_page")
        image = images.get(number)
        if image is None:
            errors.append("%s has out-of-scope scan page %s" % (path.name, number))
            continue
        if str(page.get("printed_page")) != image["printed_page"]:
            errors.append("%s scan page %s has the wrong printed page" % (path.name, number))
        if page.get("image_file") != image["filename"]:
            errors.append("%s scan page %s has the wrong image filename" % (path.name, number))
        if page.get("sha256", "").lower() != image["sha256"].lower():
            errors.append("%s scan page %s has the wrong image SHA-256" % (path.name, number))
        blocks = page.get("blocks", [])
        if not blocks:
            errors.append("%s scan page %s has no transcription blocks" % (path.name, number))
        for position, block in enumerate(blocks, 1):
            expected_id = "p%03d-b%02d" % (number, position)
            block_id = block.get("block_id")
            if block_id != expected_id:
                errors.append("%s expected block id %s" % (path.name, expected_id))
            if block_id in block_ids:
                errors.append("%s repeats block id %s" % (path.name, block_id))
            block_ids.add(block_id)
            if block.get("role") not in ALLOWED_ROLES:
                errors.append("%s block %s has an unknown role" % (path.name, block_id))
            if block.get("region") not in ALLOWED_REGIONS:
                errors.append("%s block %s has an unknown region" % (path.name, block_id))
            lines = block.get("lines", [])
            if not lines:
                errors.append("%s block %s has no lines" % (path.name, block_id))
            for line_number, line in enumerate(lines, 1):
                if line.get("line") != line_number:
                    errors.append("%s block %s line numbers are not sequential" % (path.name, block_id))
                text = line.get("text")
                if not isinstance(text, str) or not text:
                    errors.append("%s block %s has an empty line" % (path.name, block_id))
                    continue
                uncertain = line.get("uncertain", [])
                if not isinstance(uncertain, list):
                    errors.append("%s block %s has an invalid uncertainty list" % (path.name, block_id))
                if "\ufffd" in text and not uncertain:
                    errors.append("%s block %s hides an unreadable character" % (path.name, block_id))
        continuity = page.get("continuity", {})
        if not continuity.get("begins_with") or not continuity.get("ends_with"):
            errors.append("%s scan page %s lacks continuity anchors" % (path.name, number))
        review = page.get("review", {})
        if review.get("publication_ready"):
            errors.extend(review_record_errors(page, path.name))

    review = data.get("review", {})
    if review.get("publication_ready"):
        for field in (
            "two_independent_visual_reconciliations",
            "zero_unresolved_readings",
            "page_continuity_checked",
        ):
            if review.get(field) is not True:
                errors.append("%s claims readiness without %s" % (path.name, field))
    return errors, data


def collect_ranges(manifest: dict) -> tuple[list[str], list[dict], list[Path]]:
    errors: list[str] = []
    ranges: list[dict] = []
    missing: list[Path] = []
    for start, end, path in RANGE_SPECS:
        range_errors, data = validate_range(path, start, end, manifest)
        errors.extend(range_errors)
        if data is None:
            missing.append(path)
        else:
            ranges.append(data)
    return errors, ranges, missing


def page_has_uncertainty(page: dict) -> bool:
    if page.get("unresolved"):
        return True
    for block in page.get("blocks", []):
        for line in block.get("lines", []):
            if line.get("uncertain") or "\ufffd" in line.get("text", ""):
                return True
    return False


def review_record_errors(page: dict, label: str) -> list[str]:
    errors: list[str] = []
    number = page.get("scan_page")
    review = page.get("review", {})
    records = review.get("visual_reconciliations", [])
    if not isinstance(records, list) or len(records) < 2:
        return ["%s scan page %s lacks two visual reconciliations" % (label, number)]
    reviewer_ids = []
    for position, record in enumerate(records, 1):
        prefix = "%s scan page %s review %s" % (label, number, position)
        reviewer_id = record.get("reviewer_id")
        reviewer_kind = record.get("reviewer_kind")
        method = record.get("method")
        if not isinstance(reviewer_id, str) or not reviewer_id.strip():
            errors.append("%s lacks reviewer_id" % prefix)
        else:
            reviewer_ids.append(reviewer_id)
        if not isinstance(reviewer_kind, str) or not reviewer_kind.strip():
            errors.append("%s lacks reviewer_kind" % prefix)
        if not isinstance(method, str) or not method.strip():
            errors.append("%s lacks method" % prefix)
        if record.get("completed") is not True:
            errors.append("%s is not complete" % prefix)
        if record.get("independent") is not True:
            errors.append("%s is not marked independent" % prefix)
    if len(reviewer_ids) != len(set(reviewer_ids)):
        errors.append("%s scan page %s repeats a reviewer id" % (label, number))
    if review.get("page_continuity_checked") is not True:
        errors.append("%s scan page %s continuity is not checked" % (label, number))
    if page_has_uncertainty(page):
        errors.append("%s scan page %s still has unresolved text" % (label, number))
    return errors


def staging_gate(ranges: list[dict]) -> list[str]:
    errors: list[str] = []
    if len(ranges) != 2:
        return ["both transcription range files are required for staging"]
    pages = [page for item in ranges for page in item.get("pages", [])]
    if [page.get("scan_page") for page in pages] != list(range(50, 86)):
        errors.append("transcription pages are not 50 through 85 exactly once")
    for item in ranges:
        review = item.get("review", {})
        for field in (
            "continuous_transcription",
            "all_pages_visually_reconciled",
            "page_continuity_checked",
        ):
            if review.get(field) is not True:
                errors.append("%s must be true before staging" % field)
    for page in pages:
        number = page.get("scan_page")
        review = page.get("review", {})
        if review.get("visual_reconciled") is not True:
            errors.append("scan page %s is not visually reconciled" % number)
        if review.get("page_continuity_checked") is not True:
            errors.append("scan page %s continuity is not checked" % number)
        if page_has_uncertainty(page):
            errors.append("scan page %s still has unresolved text" % number)
    return errors


def publication_gate(manifest: dict, ranges: list[dict]) -> list[str]:
    errors = staging_gate(ranges)
    review = manifest.get("review", {})
    for field in (
        "continuous_transcription",
        "page_continuity_checked",
        "zero_unresolved_readings",
        "two_independent_visual_reconciliations",
        "publication_ready",
    ):
        if review.get(field) is not True:
            errors.append("manifest %s must be true before library output" % field)
    for item in ranges:
        range_review = item.get("review", {})
        for field in (
            "two_independent_visual_reconciliations",
            "zero_unresolved_readings",
            "page_continuity_checked",
            "publication_ready",
        ):
            if range_review.get(field) is not True:
                errors.append("range %s must be true before library output" % field)
        for page in item.get("pages", []):
            page_review = page.get("review", {})
            errors.extend(review_record_errors(page, "publication"))
            if page_review.get("publication_ready") is not True:
                errors.append("scan page %s is not publication ready" % page.get("scan_page"))
    return errors


def page_text(page: dict) -> str:
    return "\n".join(
        line["text"]
        for block in page.get("blocks", [])
        for line in block.get("lines", [])
    ).strip()


def build_library(manifest: dict, ranges: list[dict]) -> dict:
    work_id = manifest["scope"]["work_id"]
    title = "خدمة القداس الإلهي للقديس يوحنا الذهبي الفم"
    work = {
        "work_id": work_id,
        "edition_of": "divine-liturgy-chrysostom",
        "title": title,
        "author": "The Orthodox Church, attributed to St John Chrysostom",
        "editor": "Archimandrite Gerasimos Messara",
        "language": "ar",
        "date": "4th-5th c.; Beirut edition 1890",
        "translator": None,
        "pub_year": 1890,
        "source": "1890 Beirut edition",
        "publisher": "al-Matbaah al-Adabiyyah, Beirut",
        "source_url": manifest["source"]["access_url"],
        "source_class": "liturgical",
        "description": "Source: 1890 Beirut edition.",
        "digitized": "OrthodoxOnline upload on Scribd",
        "rights": "Public domain underlying text",
        "scan_license": "Attribution Non-Commercial (BY-NC)",
        "scan_distribution": "Scan images are not redistributed by Plithos",
        "saint": "Saint John Chrysostom, Archbishop of Constantinople",
        "is_saint": True,
    }
    pages = [page for item in ranges for page in item["pages"]]
    units = []
    for ordinal, page in enumerate(pages, 1):
        number = page["scan_page"]
        units.append({
            "unit_id": "%s::p%03d" % (work_id, number),
            "work_id": work_id,
            "work_title": title,
            "author": work["author"],
            "source_class": "liturgical",
            "ordinal": ordinal,
            "citation_anchor": "1890 edition, p. %s" % page["printed_page"],
            "source_page": number,
            "text": page_text(page),
        })
    review_records = [
        record
        for item in ranges
        for page in item.get("pages", [])
        for record in page.get("review", {}).get("visual_reconciliations", [])
    ]
    return {
        "work": work,
        "units": units,
        "source_review": {
            "source_manifest": "tools/manuscripts/%s" % MANIFEST.name,
            "range_files": [path.name for _, _, path in RANGE_SPECS],
            "scan_pages": [50, 85],
            "scan_images_committed": False,
            "zero_unresolved_readings": manifest["review"].get(
                "zero_unresolved_readings", False
            ),
            "two_independent_visual_reconciliations": manifest["review"].get(
                "two_independent_visual_reconciliations", False
            ),
            "reviewer_kinds": sorted(set(
                record.get("reviewer_kind", "") for record in review_records
                if record.get("reviewer_kind")
            )),
            "review_methods": sorted(set(
                record.get("method", "") for record in review_records
                if record.get("method")
            )),
            "qualified_human_arabic_review": manifest["review"].get(
                "qualified_human_arabic_review", {}
            ),
            "publication_ready": manifest["review"].get("publication_ready", False),
        },
    }


def write_staging(manifest: dict, ranges: list[dict]) -> list[str]:
    errors = staging_gate(ranges)
    if errors:
        return errors
    output = build_library(manifest, ranges)
    output["source_review"]["publication_ready"] = False
    write_json(STAGING, output)
    print("WROTE %s" % STAGING.relative_to(ROOT))
    return []


def write_library(manifest: dict, ranges: list[dict]) -> list[str]:
    errors = publication_gate(manifest, ranges)
    if errors:
        return errors
    expected = build_library(manifest, ranges)
    if not STAGING.is_file():
        return ["staging file is missing; run with --write-staging first"]
    actual = load_json(STAGING)
    staged = build_library(manifest, ranges)
    staged["source_review"]["publication_ready"] = False
    if actual != staged:
        return ["staging file is stale or review flags changed"]
    write_json(FINAL, {"work": expected["work"], "units": expected["units"]})
    print("WROTE %s" % FINAL.relative_to(ROOT))
    print("The works index and served page remain unchanged.")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate source and transcription artifacts")
    parser.add_argument("--verify-images", type=Path, help="verify the 36 working page images")
    parser.add_argument("--print-map", action="store_true", help="print the source page and asset map")
    parser.add_argument("--write-staging", action="store_true", help="write an unserved library-schema staging artifact")
    parser.add_argument("--write-library", action="store_true", help="write the final work only after every review gate passes")
    args = parser.parse_args()

    manifest = load_json(MANIFEST)
    errors = validate_manifest(manifest)
    range_errors, ranges, missing = collect_ranges(manifest)
    errors.extend(range_errors)

    image_dir = args.verify_images
    if image_dir is None and default_image_dir().is_dir():
        image_dir = default_image_dir()
    if image_dir is not None:
        errors.extend(verify_images(image_dir, manifest))

    if args.print_map:
        for page in manifest["working_images"]["pages"]:
            print(
                "%d\t%s\t%s\t%s"
                % (page["scan_page"], page["filename"], page["sha256"], asset_url(page))
            )

    if args.write_staging:
        errors.extend(write_staging(manifest, ranges))
    if args.write_library:
        errors.extend(write_library(manifest, ranges))

    if errors:
        for error in errors:
            print("FAIL %s" % error, file=sys.stderr)
        return 1

    verified = 36 if image_dir is not None else 0
    print(
        "OK Messara 1890 source: scan pages 50-85, %d image(s) verified, "
        "%d transcription range(s) present, %d range(s) pending"
        % (verified, len(ranges), len(missing))
    )
    if missing:
        for path in missing:
            print("PENDING %s" % path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
