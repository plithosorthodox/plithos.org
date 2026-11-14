#!/usr/bin/env python3
"""Validate and build lazy Library catalog metadata translations.

The historical text and edition citations remain exactly as published. This
builder covers reader-facing catalog metadata only: title, description,
caution, and an optional display form of the work date. Author, topic,
purpose, period, and language labels remain in the Library RLEX table.

Each language has one source file under tools/library_catalog_i18n. A
production payload is written only when every required title, description,
caution, and newly introduced catalog term in that language is present.
Missing data therefore falls back to canonical metadata in the page, but an
incomplete translation can never be published by this builder.

    python tools/build_library_catalog_i18n.py --check
    python tools/build_library_catalog_i18n.py --check --strict
    python tools/build_library_catalog_i18n.py --write --language el
    python tools/build_library_catalog_i18n.py --verify --language el
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"
INDEX = ROOT / "data" / "library" / "works-index.json"
SOURCE_DIR = ROOT / "tools" / "library_catalog_i18n"
OUTPUT = ROOT / "data" / "library"
FORMAT = "plithos-library-catalog-i18n"
SOURCE_FORMAT = FORMAT + "-language-source"
SOURCE_VERSION = 1
VERSION = 3

UI_LANGS = (
    "el", "ru", "ka", "ro", "sr", "uk", "ar", "es", "pt", "it",
    "fr", "de", "zh", "ja", "ko", "sw", "hi", "hy", "arc", "bn",
    "ur", "bg",
)
REQUIRED_FIELDS = ("title", "description", "caution")
OPTIONAL_FIELDS = ("date",)
ALLOWED_FIELDS = set(REQUIRED_FIELDS + OPTIONAL_FIELDS)
REQUIRED_TERMS = (
    "19th century",
    "20th century",
    "21st century",
    "Anonymous",
    "Evagrius Scholasticus",
    "Orthodox Church",
    "The Great Church of Constantinople, Patriarch Anthimus VII and the Holy Synod",
    "The eighty-seven bishops at Carthage",
)
FORBIDDEN = {
    "\u2013": "en dash",
    "\u2014": "em dash",
    "\u2018": "curly single quote",
    "\u2019": "curly single quote",
    "\u201c": "curly double quote",
    "\u201d": "curly double quote",
    "\ufffd": "replacement character",
    "\u25a1": "empty-square placeholder",
}
CORPUS_HEAD = "const CORPUS = "


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_core_works():
    src = PAGE.read_text(encoding="utf-8")
    start = src.index(CORPUS_HEAD) + len(CORPUS_HEAD)
    end = src.index("\n", start)
    corpus = json.loads(src[start:end].rstrip().rstrip(";"))
    return corpus.get("works") or []


def read_catalog():
    works = list(read_core_works())
    works.extend(read_json(INDEX))
    by_id = {}
    for work in works:
        work_id = work.get("work_id")
        if not work_id:
            raise ValueError("catalog work without work_id")
        if work_id in by_id:
            raise ValueError("duplicate catalog work_id: " + work_id)
        by_id[work_id] = work
    return by_id


def required_for(work):
    return tuple(field for field in REQUIRED_FIELDS if work.get(field))


def canonical_fingerprint(catalog):
    rows = []
    for work_id in sorted(catalog):
        work = catalog[work_id]
        row = {"work_id": work_id}
        for field in sorted(ALLOWED_FIELDS):
            if work.get(field) is not None:
                row[field] = work.get(field)
        rows.append(row)
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_text(lang, work_id, field, value, errors):
    where = "%s/%s/%s" % (lang, work_id, field)
    if not isinstance(value, str) or not value.strip():
        errors.append(where + ": value must be a nonempty string")
        return
    if value != value.strip():
        errors.append(where + ": leading or trailing whitespace")
    if "<" in value or ">" in value:
        errors.append(where + ": HTML is not allowed")
    if any(ord(ch) < 32 and ch not in "\n\t" for ch in value):
        errors.append(where + ": control character is not allowed")
    for char, name in FORBIDDEN.items():
        if char in value:
            errors.append(where + ": " + name + " is not allowed")


def validate_source(source, catalog, expected_lang=None):
    errors = []
    if source.get("format") != SOURCE_FORMAT:
        errors.append("source format must be " + SOURCE_FORMAT)
    if source.get("version") != SOURCE_VERSION:
        errors.append("source version must be %d" % SOURCE_VERSION)
    expected_fingerprint = canonical_fingerprint(catalog)
    if source.get("catalog_sha256") != expected_fingerprint:
        errors.append("source catalog_sha256 must be " + expected_fingerprint)
    lang = source.get("language")
    if lang not in UI_LANGS:
        errors.append("unknown UI language: " + str(lang))
        return errors
    if expected_lang and lang != expected_lang:
        errors.append("source language %s does not match filename %s" %
                      (lang, expected_lang))
    entries = source.get("works")
    if not isinstance(entries, dict):
        return errors + [lang + ": works must be an object"]
    for work_id, fields in entries.items():
        if work_id not in catalog:
            errors.append(lang + ": unknown work_id: " + work_id)
            continue
        if not isinstance(fields, dict):
            errors.append(lang + "/" + work_id + ": value must be an object")
            continue
        unknown = sorted(set(fields) - ALLOWED_FIELDS)
        if unknown:
            errors.append(lang + "/" + work_id +
                          ": unknown field(s): " + ", ".join(unknown))
        for field, value in fields.items():
            if field in ALLOWED_FIELDS:
                validate_text(lang, work_id, field, value, errors)
                canonical = catalog[work_id].get(field)
                if field in ("title", "description", "caution") and canonical:
                    native_title = (field == "title" and
                                    catalog[work_id].get("language") == lang)
                    if (value.casefold() == str(canonical).casefold() and
                            not native_title):
                        errors.append(lang + "/" + work_id + "/" + field +
                                      ": untranslated canonical text")
                if field in ("description", "caution") and canonical:
                    ratio = len(value) / max(1, len(str(canonical)))
                    if ratio < 0.20 or ratio > 3.50:
                        errors.append(lang + "/" + work_id + "/" + field +
                                      ": suspicious length ratio %.2f" % ratio)
    terms = source.get("terms")
    if not isinstance(terms, dict):
        errors.append(lang + ": terms must be an object")
    else:
        unknown_terms = sorted(set(terms) - set(REQUIRED_TERMS))
        if unknown_terms:
            errors.append(lang + ": unknown term(s): " +
                          ", ".join(unknown_terms))
        for term, value in terms.items():
            if term in REQUIRED_TERMS:
                validate_text(lang, "terms", term, value, errors)
    return errors


def read_sources(catalog, only=None):
    languages = {}
    errors = []
    if not SOURCE_DIR.exists():
        return languages, errors
    for path in sorted(SOURCE_DIR.glob("*.json")):
        expected = path.stem
        if only and expected != only:
            continue
        source = read_json(path)
        errors.extend(validate_source(source, catalog, expected))
        lang = source.get("language")
        if lang in languages:
            errors.append("duplicate language source: " + str(lang))
        elif lang in UI_LANGS:
            languages[lang] = source
    return languages, errors


def coverage(source, catalog):
    entries = source.get("works") or {}
    required = 0
    present = 0
    complete_works = 0
    missing = []
    for work_id in sorted(catalog):
        need = required_for(catalog[work_id])
        required += len(need)
        have = entries.get(work_id) or {}
        absent = [field for field in need if not have.get(field)]
        present += len(need) - len(absent)
        if absent:
            missing.append((work_id, absent))
        else:
            complete_works += 1
    missing_terms = [term for term in REQUIRED_TERMS
                     if not (source.get("terms") or {}).get(term)]
    return {
        "required": required,
        "present": present,
        "complete_works": complete_works,
        "total_works": len(catalog),
        "missing": missing,
        "missing_terms": missing_terms,
        "complete": not missing and not missing_terms,
    }


def payload(lang, source, catalog, fingerprint):
    entries = source.get("works") or {}
    works = {}
    for work_id in sorted(catalog):
        fields = entries.get(work_id) or {}
        if fields:
            works[work_id] = {
                field: fields[field]
                for field in sorted(fields)
                if field in ALLOWED_FIELDS
            }
    return {
        "format": FORMAT,
        "version": VERSION,
        "language": lang,
        "catalog_sha256": fingerprint,
        "terms": {term: source["terms"][term] for term in REQUIRED_TERMS},
        "works": works,
    }


def serialise(doc):
    return (json.dumps(doc, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def output_path(lang):
    return OUTPUT / ("catalog-i18n.v%d.%s.json" % (VERSION, lang))


def selected_languages(args, languages):
    if args.language:
        if args.language not in UI_LANGS:
            raise ValueError("unknown UI language: " + args.language)
        return [args.language]
    if args.strict:
        return list(UI_LANGS)
    return sorted(languages)


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    action.add_argument("--verify", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="require every non-English UI language")
    parser.add_argument("--language", choices=UI_LANGS)
    args = parser.parse_args()

    try:
        catalog = read_catalog()
        languages, errors = read_sources(catalog, args.language)
        chosen = selected_languages(args, languages)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("library catalog i18n: " + str(exc), file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print("ERROR " + error, file=sys.stderr)
        return 1

    fingerprint = canonical_fingerprint(catalog)
    page_source = PAGE.read_text(encoding="utf-8")
    match = re.search(r'var CATALOG_I18N_SHA="([0-9a-f]{64})";', page_source)
    if not match or match.group(1) != fingerprint:
        print("library.html catalog fingerprint is missing or stale: " +
              fingerprint, file=sys.stderr)
        return 1
    reports = {}
    incomplete = []
    for lang in chosen:
        report = coverage(languages.get(lang) or {}, catalog)
        reports[lang] = report
        print("%s: %d/%d fields, %d/%d works complete" % (
            lang, report["present"], report["required"],
            report["complete_works"], report["total_works"]))
        if not report["complete"]:
            incomplete.append(lang)
            for work_id, fields in report["missing"][:5]:
                print("  missing %s: %s" % (work_id, ", ".join(fields)))
            extra = len(report["missing"]) - 5
            if extra > 0:
                print("  and %d more incomplete works" % extra)
            if report["missing_terms"]:
                print("  missing terms: " + ", ".join(report["missing_terms"]))

    if args.write or args.verify:
        if incomplete:
            print("refusing payload operation for incomplete language(s): " +
                  ", ".join(incomplete), file=sys.stderr)
            return 1
        if not chosen:
            print("no complete language selected", file=sys.stderr)
            return 1
        for lang in chosen:
            raw = serialise(payload(lang, languages[lang], catalog, fingerprint))
            path = output_path(lang)
            if args.write:
                path.write_bytes(raw)
                print("wrote %s (%d bytes)" % (path.relative_to(ROOT), len(raw)))
            else:
                if not path.exists() or path.read_bytes() != raw:
                    print("stale or missing payload: " + str(path.relative_to(ROOT)),
                          file=sys.stderr)
                    return 1
                print("verified " + str(path.relative_to(ROOT)))

    if args.strict and incomplete:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
