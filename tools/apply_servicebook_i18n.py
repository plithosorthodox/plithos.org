#!/usr/bin/env python3
"""Install the Service Books guide and catalog translations.

The compact manuscript is the translation authority. This tool installs its
reader-facing labels in library.html, adds its catalog fields and terms to the
twenty-two catalog source files, and advances their catalog fingerprint.

    python tools/apply_servicebook_i18n.py --import-source tmp/servicebook-i18n.json --write
    python tools/apply_servicebook_i18n.py --check
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
CATALOG_DIR = ROOT / "tools" / "library_catalog_i18n"
MANUSCRIPT = ROOT / "tools" / "manuscripts" / "servicebook-i18n.json"
UI_LANGS = (
    "en", "el", "ru", "ka", "ro", "sr", "uk", "ar", "es", "pt",
    "it", "fr", "de", "zh", "ja", "ko", "sw", "hi", "hy", "arc",
    "bn", "ur", "bg",
)
UI_KEYS = (
    "secServiceBooks", "secServiceBooksDesc", "serviceGuideTitle",
    "completeBook", "openFacsimile", "authMinister", "authAuthorization",
    "authCondition", "authForm", "authSource", "readerOfficesTitle",
    "readerOfficesText", "readerOfficesMinister",
    "readerOfficesAuthorization", "deaconCommunionTitle",
    "deaconCommunionMinister", "deaconCommunionAuthorization",
    "emergencyBaptismTitle", "emergencyBaptismMinister",
    "emergencyBaptismAuthorization", "emergencyBaptismCondition",
    "emergencyBaptismForm", "baptismalExorcismsTitle",
    "baptismalExorcismsMinister", "baptismalExorcismsCondition",
    "formalExorcismsTitle", "formalExorcismsMinister",
    "formalExorcismsCondition", "commonProtectionTitle",
    "commonProtectionMinister",
)
CATALOG_KEYS = {
    "akathist-ambrose-optina-sr": "catalogAkathistAmbrose",
    "euchology-shann-1891": "catalogEuchologyShann",
    "great-euchologion-1869-el": "catalogGreatEuchologion",
    "service-book-hapgood-1906": "catalog",
}
TERM_KEYS = {
    "21st century": "century21",
    "Orthodox Church": "orthodoxChurch",
}
START = "/* SERVICE BOOK I18N START */"
END = "/* SERVICE BOOK I18N END */"
FORBIDDEN = "\u2013\u2014\u2018\u2019\u201c\u201d\ufffd\u25a1"
BAPTISM_FORMULA = (
    "The servant of God, [name], is baptized, in the name of the Father, "
    "Amen. And of the Son, Amen. And of the Holy Spirit. Amen."
)


def encoded(value, compact=False):
    if compact:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2)
    return (text + "\n").encode("utf-8")


def read_core_works(source):
    needle = "const CORPUS = "
    start = source.index(needle) + len(needle)
    end = source.index("\n", start)
    return json.loads(source[start:end].rstrip().rstrip(";"))["works"]


def fingerprint(page_source):
    works = list(read_core_works(page_source))
    works.extend(json.loads(INDEX.read_text(encoding="utf-8")))
    rows = []
    for work in sorted(works, key=lambda row: row["work_id"]):
        row = {"work_id": work["work_id"]}
        for field in ("caution", "date", "description", "title"):
            if work.get(field) is not None:
                row[field] = work[field]
        rows.append(row)
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate(raw):
    if set(raw) != set(UI_LANGS):
        missing = sorted(set(UI_LANGS) - set(raw))
        extra = sorted(set(raw) - set(UI_LANGS))
        raise ValueError("language mismatch; missing %s; extra %s" %
                         (", ".join(missing), ", ".join(extra)))
    compact = {}
    for lang in UI_LANGS:
        source = raw[lang]
        absent = [key for key in UI_KEYS if not source.get(key)]
        absent += [key for key in TERM_KEYS.values() if not source.get(key)]
        absent += [key for key in CATALOG_KEYS.values()
                   if not isinstance(source.get(key), dict)]
        if absent:
            raise ValueError("%s missing %s" % (lang, ", ".join(absent)))
        entry = {key: source[key] for key in UI_KEYS}
        entry.update({key: source[key] for key in TERM_KEYS.values()})
        for key in CATALOG_KEYS.values():
            fields = source[key]
            entry[key] = {name: fields[name]
                          for name in ("title", "description")}
        for value in walk_strings(entry):
            bad = [char for char in FORBIDDEN if char in value]
            if bad:
                raise ValueError("%s contains forbidden punctuation U+%04X" %
                                 (lang, ord(bad[0])))
        compact[lang] = entry
    for lang in UI_LANGS:
        if BAPTISM_FORMULA not in compact[lang]["emergencyBaptismForm"]:
            raise ValueError(lang + " does not preserve the Baptism formula")
    return compact


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def page_with_translations(page, manuscript, catalog_hash):
    ui = {lang: {key: manuscript[lang][key] for key in UI_KEYS}
          for lang in UI_LANGS}
    block = (START + "\nconst SERVICE_BOOK_I18N=" +
             json.dumps(ui, ensure_ascii=False, sort_keys=True,
                        separators=(",", ":")) + ";\n" +
             "Object.keys(SERVICE_BOOK_I18N).forEach(function(lang){" +
             "if(RLEX[lang])Object.assign(RLEX[lang],SERVICE_BOOK_I18N[lang]);" +
             "});\n" + END)
    if START in page:
        page = re.sub(re.escape(START) + r".*?" + re.escape(END), block,
                      page, flags=re.S)
    else:
        page = page.replace("\nlet uiLang=", "\n" + block + "\nlet uiLang=", 1)
    page, count = re.subn(r'var CATALOG_I18N_SHA="[0-9a-f]{64}";',
                          'var CATALOG_I18N_SHA="%s";' % catalog_hash, page)
    if count != 1:
        raise ValueError("catalog fingerprint assignment not found")
    return page


def expected_sources(manuscript, catalog_hash):
    expected = {}
    for lang in UI_LANGS:
        if lang == "en":
            continue
        path = CATALOG_DIR / (lang + ".json")
        data = json.loads(path.read_text(encoding="utf-8"))
        data["catalog_sha256"] = catalog_hash
        terms = data.setdefault("terms", {})
        for term, key in TERM_KEYS.items():
            terms[term] = manuscript[lang][key]
        works = data.setdefault("works", {})
        for work_id, key in CATALOG_KEYS.items():
            works[work_id] = dict(manuscript[lang][key])
        expected[path] = data
    return expected


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--import-source")
    args = parser.parse_args()
    try:
        if args.import_source:
            source = Path(args.import_source)
            if not source.is_absolute():
                source = ROOT / source
            manuscript = validate(json.loads(source.read_text(encoding="utf-8")))
            if args.write:
                MANUSCRIPT.write_bytes(encoded(manuscript))
        else:
            manuscript = validate(json.loads(
                MANUSCRIPT.read_text(encoding="utf-8")))
        page = PAGE.read_text(encoding="utf-8")
        catalog_hash = fingerprint(page)
        expected_page = page_with_translations(page, manuscript, catalog_hash)
        english_start = expected_page.index("Object.assign(RLEX.en,{")
        english_end = expected_page.index("});", english_start)
        if BAPTISM_FORMULA not in expected_page[english_start:english_end]:
            raise ValueError("English page copy does not preserve the Baptism formula")
        sources = expected_sources(manuscript, catalog_hash)
        if args.write:
            PAGE.write_text(expected_page, encoding="utf-8")
            for path, data in sources.items():
                path.write_bytes(encoded(data))
        stale = []
        if PAGE.read_text(encoding="utf-8") != expected_page:
            stale.append(str(PAGE.relative_to(ROOT)))
        for path, data in sources.items():
            if json.loads(path.read_text(encoding="utf-8")) != data:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            raise ValueError("stale: " + ", ".join(stale))
        print("service-book i18n: %d languages, catalog %s" %
              (len(UI_LANGS), catalog_hash))
        return 0
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print("service-book i18n: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
