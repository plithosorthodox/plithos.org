#!/usr/bin/env python3
"""Check translation source keys, values, and published-bundle parity."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import build_saint_lives
import build_saint_terms
import saint_info_en
from translation_checks import validate_pairs


def load_text(path):
    spec = importlib.util.spec_from_file_location("check_" + path.parent.name + "_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(getattr(mod, "TEXT", {})), mod


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    problems = []
    families = (
        ("saint_terms", build_saint_terms.english(), "saint-terms.v5", True),
        ("saint_lives", build_saint_lives.english(), "saint-lives.v6", False),
        ("saint_info", saint_info_en.load(), "saint-info.v1", False),
    )
    for dirname, english, bundle_stem, expands in families:
        for path in sorted((TOOLS / dirname).glob("*.py")):
            if path.stem.startswith("_"):
                continue
            text, mod = load_text(path)
            produced = {}
            if expands and hasattr(mod, "expand"):
                produced.update(mod.expand(set(english)))
            produced.update(text)
            extra = sorted(set(produced) - set(english))
            problems.extend("%s/%s: unknown source key %r" % (dirname, path.stem, k)
                            for k in extra)
            pairs = []
            for key, value in sorted(produced.items()):
                if key not in english:
                    continue
                if dirname == "saint_info":
                    for field, rendered in sorted(value.items()):
                        if field in english[key] and isinstance(rendered, str):
                            pairs.append(("%s.%s" % (key, field), english[key][field], rendered))
                else:
                    pairs.append((key, key if dirname == "saint_terms" else english[key], value))
            problems.extend("%s/%s: %s" % (dirname, path.stem, e)
                            for e in validate_pairs(path.stem, pairs))
            bundle = ROOT / "data" / ("%s.%s.json" % (bundle_stem, path.stem))
            if bundle.exists():
                published = json.loads(bundle.read_text(encoding="utf-8"))
                if len(published) >= len(english) and set(published) != set(english):
                    missing = sorted(set(english) - set(published))
                    extra_published = sorted(set(published) - set(english))
                    problems.append("%s/%s: published source-key coverage differs "
                                    "(missing %d, extra %d)" %
                                    (dirname, path.stem, len(missing),
                                     len(extra_published)))
                for key, value in sorted(produced.items()):
                    if published.get(key) != value:
                        problems.append("%s/%s: source/published mismatch at %r"
                                        % (dirname, path.stem, key))
            elif produced:
                problems.append("%s/%s: published bundle is missing" % (dirname, path.stem))
    if problems:
        print("%d translation problem(s):" % len(problems))
        for problem in problems[:100]:
            print("  " + problem)
        if len(problems) > 100:
            print("  ... and %d more" % (len(problems) - 100))
        return 1
    print("translation sources, values, references, scripts, and bundles agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
