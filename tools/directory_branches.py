#!/usr/bin/env python3
"""Build every parish-scale branch of the Churches directory together.

Country modules retain their own source checks and exact row counts. This
small coordinator prevents two country passes from silently claiming the
same parent or row id, then writes and checks each module through its own
public API.
"""

import argparse
import sys

import directory_estonia
import directory_finland
import directory_direct
import directory_japan
import directory_korea
import directory_latvia
import directory_lithuania
import directory_northwest_europe


MODULES = (
    directory_estonia,
    directory_finland,
    directory_direct,
    directory_japan,
    directory_korea,
    directory_latvia,
    directory_lithuania,
    directory_northwest_europe,
)


def module_payloads():
    return [(module, module.build()) for module in MODULES]


def build():
    payloads = {}
    row_ids = set()
    for module, built in module_payloads():
        for parent, payload in built.items():
            if parent in payloads:
                raise ValueError("duplicate branch parent: %s" % parent)
            for row in payload.get("rows") or []:
                row_id = row.get("id")
                if not row_id or row_id in row_ids:
                    raise ValueError("duplicate or missing branch row id: %s"
                                     % row_id)
                row_ids.add(row_id)
            payloads[parent] = payload
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    out = {}
    for module, built in module_payloads():
        subset = {parent: payloads[parent] for parent in built}
        for parent, spec in module.manifest(subset).items():
            if parent in out:
                raise ValueError("duplicate branch manifest parent: %s" % parent)
            out[parent] = spec
    return dict(sorted(out.items()))


def write(payloads):
    for module, built in module_payloads():
        module.write({parent: payloads[parent] for parent in built})


def problems(payloads):
    errors = []
    for module, built in module_payloads():
        subset = {parent: payloads[parent] for parent in built}
        errors.extend(module.problems(subset))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory branches: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("%d branch parents, %d subordinate bodies"
          % (len(payloads),
             sum(len(payload["rows"]) for payload in payloads.values())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
