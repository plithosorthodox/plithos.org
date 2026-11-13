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
DRAFT_GLOB = "balamand_1628_chrysostom_pages_*_draft.json"
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
    drafts = sorted(MANIFEST.parent.glob(DRAFT_GLOB))
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

    errors = validate_manifest(manifest)
    draft_errors, draft_count = validate_drafts()
    errors.extend(draft_errors)
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
