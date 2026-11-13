#!/usr/bin/env python3
"""Acquire and audit the 1628 Balamand Arabic liturgy manuscript.

This helper keeps source acquisition and transcription review separate from
the served Library. It does not OCR, normalize, align, or publish liturgical
text. Its jobs are limited to source integrity, page-level provenance, and
correctly oriented LOC image downloads for human transcription.

Examples:

    python tools/balamand_1628.py --check
    python tools/balamand_1628.py --print-map
    python tools/balamand_1628.py --verify-pdf C:/path/to/wdl7078.pdf
    python tools/balamand_1628.py --download-pdf C:/path/to/wdl7078.pdf
    python tools/balamand_1628.py --download-images C:/path/to/pages
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "manuscripts" / "balamand_1628_chrysostom.json"
RANGE_DRAFT_GLOB = "balamand_1628_chrysostom_pages_[0-9][0-9]_[0-9][0-9]_draft.json"
COMBINED_DRAFT = (
    MANIFEST.parent / "balamand_1628_chrysostom_combined_draft.json"
)
USER_AGENT = "Plithos source audit/1.0 (+https://plithos.org/)"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def loc_image_id(pdf_page: int) -> str:
    """Return the LOC image stem for an interior PDF page."""
    if pdf_page < 3:
        raise ValueError("interior manuscript pages begin after the cover leaves")
    return "bala00003_%03dr_%03dv_v" % (pdf_page - 1, pdf_page - 2)


def iiif_url(image_id: str, size: str = "pct:50") -> str:
    service = "service:gdc:gdcwdl:wd:l_:07:07:8:wdl_07078:%s" % image_id
    return "https://tile.loc.gov/image-services/iiif/%s/full/%s/0/default.jpg" % (
        service,
        size,
    )


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pdf(path: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    source = manifest["source"]
    if not path.is_file():
        return ["PDF does not exist: %s" % path]
    size = path.stat().st_size
    if size != source["bytes"]:
        errors.append("PDF size is %d, expected %d" % (size, source["bytes"]))
    for algorithm in ("sha1", "sha256"):
        actual = digest(path, algorithm)
        expected = source[algorithm]
        if actual.lower() != expected.lower():
            errors.append(
                "%s is %s, expected %s" % (algorithm.upper(), actual, expected)
            )
    return errors


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    forbidden = ("\u2013", "\u2014")
    raw = MANIFEST.read_text(encoding="utf-8")
    if any(mark in raw for mark in forbidden):
        errors.append("manifest contains an en dash or em dash")

    scope = manifest.get("scope", {})
    start = scope.get("start", {})
    end = scope.get("end", {})
    next_work = scope.get("next_work", {})
    expected = (
        (start, 40, "left"),
        (end, 66, "left"),
        (next_work, 67, "right"),
    )
    for item, page, side in expected:
        if item.get("pdf_page") != page:
            errors.append("boundary page is not %d" % page)
        if item.get("image_side") != side:
            errors.append("PDF page %d side is not %s" % (page, side))
        wanted = loc_image_id(page)
        if item.get("loc_image_id") != wanted:
            errors.append("PDF page %d LOC image should be %s" % (page, wanted))

    source = manifest.get("source", {})
    if source.get("bytes") != 102146031:
        errors.append("source byte count changed")
    if source.get("sha1", "").lower() != "30cdaa4d78f60790c7318e2d3cd9f3556a3ec468":
        errors.append("source SHA1 changed")

    for segment in manifest.get("segments", []):
        page = segment.get("pdf_page")
        if segment.get("loc_image_id") != loc_image_id(page):
            errors.append("segment %s has a mismatched LOC image" % segment.get("id"))
        review = segment.get("review", {})
        pending = review.get("pending_features", [])
        if pending and segment.get("publication_ready"):
            errors.append(
                "segment %s is marked publication ready with pending features"
                % segment.get("id")
            )
        if not pending and not review.get("independent_review"):
            errors.append(
                "segment %s has no pending features but lacks independent review"
                % segment.get("id")
            )
    return errors


def validate_drafts() -> tuple[list[str], int]:
    """Keep partial manual notes bounded to the verified source range."""
    errors: list[str] = []
    pages_seen: list[int] = []
    drafts = sorted(MANIFEST.parent.glob(RANGE_DRAFT_GLOB))
    forbidden = ("\u2013", "\u2014")
    for path in drafts:
        raw = path.read_text(encoding="utf-8")
        if any(mark in raw for mark in forbidden):
            errors.append("%s contains an en dash or em dash" % path.name)
        try:
            draft = json.loads(raw)
        except ValueError as exc:
            errors.append("%s is not valid JSON: %s" % (path.name, exc))
            continue
        review = draft.get("review", {})
        if review.get("publication_ready") is not False:
            errors.append("%s must remain publication_ready false" % path.name)
        if review.get("alignment_ready") is not False:
            errors.append("%s must remain alignment_ready false" % path.name)
        if review.get("continuous_transcription") is not False:
            errors.append("%s must identify itself as partial" % path.name)
        pages = draft.get("pages", [])
        for page in pages:
            number = page.get("pdf_page")
            pages_seen.append(number)
            wanted_id = loc_image_id(number)
            if page.get("loc_image_id") != wanted_id:
                errors.append("%s PDF %s has a mismatched LOC image" %
                              (path.name, number))
            sides = [x.get("side", x.get("image_side"))
                     for x in page.get("surfaces", [])]
            if sides != ["right", "left"]:
                errors.append("%s PDF %s is not ordered right then left" %
                              (path.name, number))
    if drafts and pages_seen != list(range(40, 67)):
        errors.append("draft pages must cover PDF 40 through 66 exactly once")
    if drafts:
        final = json.loads(drafts[-1].read_text(encoding="utf-8"))
        final_raw = json.dumps(final.get("pages", [])[-1], ensure_ascii=False)
        if "امين" not in final_raw:
            errors.append("final draft does not record the Chrysostom closing Amen")
        if "باسليوس" in final_raw:
            errors.append("final Chrysostom draft includes the St Basil work")
    return errors, len(drafts)


def range_drafts() -> list[tuple[Path, dict]]:
    return [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in sorted(MANIFEST.parent.glob(RANGE_DRAFT_GLOB))
    ]


def page_record_counts(pages: list[dict]) -> dict:
    surfaces = 0
    excerpt_groups = 0
    recorded_lines = 0
    uncertain_runs = 0
    pages_with_explicit_gaps = 0
    for page in pages:
        has_gap = bool(page.get("unresolved"))
        for surface in page.get("surfaces", []):
            surfaces += 1
            if surface.get("unresolved"):
                has_gap = True
            for excerpt in surface.get("excerpts", []):
                excerpt_groups += 1
                for run in excerpt.get("runs", []):
                    if run.get("text_base_letters"):
                        recorded_lines += 1
                    if run.get("confidence") not in (None, "high"):
                        uncertain_runs += 1
            for run in surface.get("confident_runs", []):
                excerpt_groups += 1
                recorded_lines += len(run.get("lines", []))
        if has_gap:
            pages_with_explicit_gaps += 1
    return {
        "page_records": len(pages),
        "surface_records": surfaces,
        "recorded_excerpt_groups": excerpt_groups,
        "recorded_lines_or_color_runs": recorded_lines,
        "uncertain_runs": uncertain_runs,
        "pages_with_explicit_gaps": pages_with_explicit_gaps,
    }


def build_combined_draft() -> dict:
    drafts = range_drafts()
    pages: list[dict] = []
    source_ranges = []
    checked_pages = []
    findings = []
    for path, draft in drafts:
        source_ranges.append(path.name)
        cross_review = draft.get("review", {}).get("cross_review", {})
        checked_pages.extend(cross_review.get("pages_checked", []))
        findings.extend(cross_review.get("findings", []))
        for original in draft.get("pages", []):
            page = json.loads(json.dumps(original, ensure_ascii=False))
            page["source_range_file"] = path.name
            pages.append(page)
    counts = page_record_counts(pages)
    return {
        "schema_version": 1,
        "draft_kind": "reconciled page-aligned excerpt transcription",
        "status": "Research draft. Not publication ready.",
        "source_manifest": MANIFEST.name,
        "work": "The Divine Liturgy of St John Chrysostom",
        "source_date": 1628,
        "language": "Arabic",
        "script": "Naskh",
        "scope": {
            "pdf_pages": [40, 66],
            "loc_surfaces": ["038v", "065r"],
            "reading_order": "On each spread, read the right surface before the left surface.",
            "next_work": "The Divine Liturgy of St Basil begins on PDF page 67 and is excluded.",
        },
        "method": {
            "source_range_files": source_ranges,
            "reconciliation": [
                "The three checked range drafts are preserved without changing their Arabic readings.",
                "Pages are joined in PDF order 40 through 66, with right surfaces before left surfaces.",
                "Every page records the range file from which its excerpts came.",
                "Gaps remain gaps. No modern service book or inferred wording fills omitted manuscript lines.",
            ],
        },
        "pages": pages,
        "review": {
            "manual_visual_pass": True,
            "independent_qualified_arabic_review": False,
            "continuous_transcription": False,
            "vocalization_complete": False,
            "rubric_boundaries_complete": False,
            "publication_ready": False,
            "alignment_ready": False,
            "page_sequence_verified": True,
            "surface_sequence_verified": True,
            "text_transition_status": (
                "Not verifiable yet. The source drafts record selected excerpts, "
                "not every line between pages."
            ),
            "range_transitions": [
                {
                    "from_pdf_page": 48,
                    "to_pdf_page": 49,
                    "page_sequence_verified": True,
                    "image_pair_checked": True,
                    "visible_folio_marks": ["45", "46"],
                    "text_continuity_verified": False,
                    "reason": "Omitted lines prevent a continuous textual join.",
                },
                {
                    "from_pdf_page": 57,
                    "to_pdf_page": 58,
                    "page_sequence_verified": True,
                    "image_pair_checked": True,
                    "visible_folio_marks": ["54", "55"],
                    "text_continuity_verified": False,
                    "reason": "Omitted lines prevent a continuous textual join.",
                },
            ],
            "coverage": counts,
            "cross_review": {
                "scope": "Independent visual spot-check only, not qualified Arabic review.",
                "pages_checked": sorted(set(checked_pages)),
                "findings": findings,
            },
            "next_required_steps": [
                "Transcribe every omitted line and rubric directly from PDF pages 40 through 66.",
                "Encode red points, punctuation, and sparse vocalization character by character.",
                "Resolve every uncertain reading without importing wording from a modern service book.",
                "Have a qualified second Arabic reader compare every character with the LOC scans.",
                "Only then verify text continuity, align the liturgy, and consider publication.",
            ],
        },
    }


def validate_combined_draft() -> list[str]:
    errors: list[str] = []
    if not COMBINED_DRAFT.is_file():
        return ["combined draft is missing; run with --write-combined"]
    raw = COMBINED_DRAFT.read_text(encoding="utf-8")
    if any(mark in raw for mark in ("\u2013", "\u2014")):
        errors.append("combined draft contains an en dash or em dash")
    try:
        actual = json.loads(raw)
    except ValueError as exc:
        return ["combined draft is not valid JSON: %s" % exc]
    expected = build_combined_draft()
    if actual != expected:
        errors.append("combined draft is stale; run with --write-combined")
    pages = actual.get("pages", [])
    if [page.get("pdf_page") for page in pages] != list(range(40, 67)):
        errors.append("combined draft pages are not PDF 40 through 66 exactly once")
    for page in pages:
        number = page.get("pdf_page")
        if page.get("loc_image_id") != loc_image_id(number):
            errors.append("combined draft PDF %s has a mismatched LOC image" % number)
        sides = [surface.get("side", surface.get("image_side"))
                 for surface in page.get("surfaces", [])]
        if sides != ["right", "left"]:
            errors.append("combined draft PDF %s is not ordered right then left" % number)
        if not page.get("source_range_file"):
            errors.append("combined draft PDF %s has no range provenance" % number)
    review = actual.get("review", {})
    for field in ("independent_qualified_arabic_review",
                  "continuous_transcription", "publication_ready",
                  "alignment_ready"):
        if review.get(field) is not False:
            errors.append("combined draft %s must remain false" % field)
    for transition in review.get("range_transitions", []):
        if transition.get("text_continuity_verified") is not False:
            errors.append("range transition must not claim textual continuity")
    final_raw = json.dumps(pages[-1] if pages else {}, ensure_ascii=False)
    if "امين" not in final_raw:
        errors.append("combined draft does not record the Chrysostom closing Amen")
    if "باسليوس" in final_raw:
        errors.append("combined draft includes the St Basil work")
    return errors


def write_combined_draft() -> None:
    output = build_combined_draft()
    COMBINED_DRAFT.write_text(
        json.dumps(output, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print("WROTE %s" % COMBINED_DRAFT.relative_to(ROOT))


def request_bytes(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request)


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError("refusing to overwrite %s" % destination)
    partial = destination.with_suffix(destination.suffix + ".part")
    try:
        with request_bytes(url) as response, partial.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
        partial.replace(destination)
    finally:
        if partial.exists():
            partial.unlink()


def download_pdf(destination: Path, manifest: dict) -> list[str]:
    download(manifest["source"]["loc_pdf_url"], destination)
    return verify_pdf(destination, manifest)


def page_map(manifest: dict):
    first = manifest["scope"]["start"]["pdf_page"]
    last = manifest["scope"]["end"]["pdf_page"]
    for page in range(first, last + 1):
        image_id = loc_image_id(page)
        yield page, image_id, iiif_url(image_id)


def download_images(destination: Path, manifest: dict) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for page, image_id, url in page_map(manifest):
        target = destination / ("pdf-%03d__%s.jpg" % (page, image_id))
        if target.exists():
            print("EXISTS %s" % target)
            continue
        print("GET    PDF %d %s" % (page, image_id))
        download(url, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the manifest")
    parser.add_argument(
        "--write-combined",
        action="store_true",
        help="reconcile the three range drafts into one checked research draft",
    )
    parser.add_argument("--print-map", action="store_true", help="print the source page map")
    parser.add_argument("--verify-pdf", type=Path, help="verify a downloaded source PDF")
    parser.add_argument("--download-pdf", type=Path, help="download and verify the LOC PDF")
    parser.add_argument(
        "--download-images",
        type=Path,
        help="download correctly oriented LOC JPEGs for PDF pages 40 through 66",
    )
    args = parser.parse_args()
    manifest = load_manifest()

    if args.write_combined:
        write_combined_draft()

    errors = validate_manifest(manifest)
    draft_errors, draft_count = validate_drafts()
    errors.extend(draft_errors)
    errors.extend(validate_combined_draft())
    if args.verify_pdf:
        errors.extend(verify_pdf(args.verify_pdf, manifest))
    if args.download_pdf:
        errors.extend(download_pdf(args.download_pdf, manifest))
    if args.download_images:
        download_images(args.download_images, manifest)
    if args.print_map:
        for page, image_id, url in page_map(manifest):
            print("PDF %d\t%s\t%s" % (page, image_id, url))

    if errors:
        for error in errors:
            print("FAIL %s" % error, file=sys.stderr)
        return 1

    segments = manifest.get("segments", [])
    ready = sum(bool(segment.get("publication_ready")) for segment in segments)
    print(
        "OK source manifest: PDF pages 40-66, %d research segment(s), %d draft range(s), %d publication ready"
        % (len(segments), draft_count, ready)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
