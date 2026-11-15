#!/usr/bin/env python3
"""Publish country contributions to shared north-west European branches.

Country modules keep the official-source audit and exact local counts. This
owner combines their rows under the regional parent IDs that also span Great
Britain, Ireland, Iceland, Norway, Sweden, and continental Europe. Bodies which answer
directly to a patriarchate remain in directory_direct instead.
"""

import argparse
import json
import sys
from pathlib import Path

import directory_albania
import directory_argentina
import directory_australia
import directory_austria
import directory_armenia
import directory_azerbaijan
import directory_belarus
import directory_belgium
import directory_benin
import directory_bosnia_montenegro
import directory_brazil
import directory_burundi
import directory_bulgaria
import directory_cambodia
import directory_cameroon
import directory_chile
import directory_congo_brazzaville
import directory_croatia
import directory_cyprus
import directory_czechia
import directory_denmark
import directory_egypt
import directory_ethiopia
import directory_france
import directory_germany
import directory_ghana
import directory_hungary
import directory_hong_kong
import directory_iceland
import directory_iberia
import directory_indonesia
import directory_ireland
import directory_iraq
import directory_jordan
import directory_italy
import directory_kazakhstan
import directory_kenya
import directory_kyrgyzstan
import directory_laos
import directory_liechtenstein
import directory_libya
import directory_luxembourg
import directory_madagascar
import directory_malawi
import directory_malta_gibraltar
import directory_mexico
import directory_microstates
import directory_netherlands
import directory_nigeria
import directory_north_atlantic
import directory_north_macedonia
import directory_norway
import directory_philippines
import directory_poland
import directory_qatar
import directory_romania
import directory_rwanda
import directory_serbia
import directory_singapore
import directory_slovenia
import directory_slovakia
import directory_sweden
import directory_switzerland
import directory_tajikistan
import directory_thailand
import directory_tunisia
import directory_turkmenistan
import directory_uganda
import directory_uzbekistan
import directory_vietnam
import directory_zambia
import directory_zimbabwe
import directory_sudan
import directory_south_sudan


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
SOURCE_MODULES = (
    directory_albania,
    directory_argentina,
    directory_austria,
    directory_armenia,
    directory_azerbaijan,
    directory_belarus,
    directory_belgium,
    directory_benin,
    directory_bosnia_montenegro,
    directory_brazil,
    directory_burundi,
    directory_bulgaria,
    directory_cambodia,
    directory_cameroon,
    directory_chile,
    directory_congo_brazzaville,
    directory_croatia,
    directory_cyprus,
    directory_czechia,
    directory_denmark,
    directory_egypt,
    directory_ethiopia,
    directory_france,
    directory_germany,
    directory_ghana,
    directory_hungary,
    directory_hong_kong,
    directory_iceland,
    directory_iberia,
    directory_ireland,
    directory_iraq,
    directory_jordan,
    directory_italy,
    directory_kazakhstan,
    directory_kenya,
    directory_kyrgyzstan,
    directory_laos,
    directory_liechtenstein,
    directory_libya,
    directory_luxembourg,
    directory_madagascar,
    directory_malawi,
    directory_malta_gibraltar,
    directory_mexico,
    directory_microstates,
    directory_netherlands,
    directory_nigeria,
    directory_north_atlantic,
    directory_north_macedonia,
    directory_norway,
    directory_poland,
    directory_qatar,
    directory_romania,
    directory_rwanda,
    directory_serbia,
    directory_singapore,
    directory_slovenia,
    directory_slovakia,
    directory_sweden,
    directory_switzerland,
    directory_tajikistan,
    directory_thailand,
    directory_tunisia,
    directory_turkmenistan,
    directory_uganda,
    directory_uzbekistan,
    directory_vietnam,
    directory_zambia,
    directory_zimbabwe,
    directory_sudan,
    directory_south_sudan,
)
DIRECT_PARENTS = {"romania", "russia"}


def payload_countries(payload):
    if isinstance(payload.get("countries"), list):
        return payload["countries"]
    return [payload["country"]]


def build():
    payloads = {}
    countries = {}
    row_ids = set()
    for module in SOURCE_MODULES:
        for parent, contribution in module.build().items():
            if parent in DIRECT_PARENTS:
                continue
            if contribution.get("v") != 1 or contribution.get("parent") != parent:
                raise ValueError("invalid contribution for %s" % parent)
            payload = payloads.setdefault(
                parent, {"v": 1, "parent": parent, "rows": []})
            countries.setdefault(parent, set()).update(
                payload_countries(contribution))
            for row in contribution.get("rows") or []:
                row_id = row.get("id")
                if not row_id or row_id in row_ids:
                    raise ValueError("duplicate or missing row id: %s" % row_id)
                row_ids.add(row_id)
                payload["rows"].append(row)
    # The Philippines module contributes to several regional branches. This
    # owner publishes the new Moscow diocesan branch and appends the
    # Ecumenical Patriarchate rows to the existing Hong Kong payload. The
    # Antiochian and ROCOR rows remain with their established branch owners.
    philippines = directory_philippines.build()
    for parent in (
            directory_philippines.PARENT,
            directory_philippines.EP_PARENT):
        contribution = philippines[parent]
        payload = payloads.setdefault(
            parent, {"v": 1, "parent": parent, "rows": []})
        countries.setdefault(parent, set()).update(
            payload_countries(contribution))
        for row in contribution["rows"]:
            row_id = row.get("id")
            if not row_id or row_id in row_ids:
                raise ValueError("duplicate or missing row id: %s" % row_id)
            row_ids.add(row_id)
            payload["rows"].append(row)
    # Indonesia contributes to the existing Singapore branches of both the
    # Ecumenical and Moscow Patriarchates. Its ROCOR bodies remain with the
    # established Australia and New Zealand branch owner in directory_korea.
    indonesia = directory_indonesia.build()
    for parent in (
            directory_indonesia.EP_PARENT,
            directory_indonesia.MP_PARENT):
        contribution = indonesia[parent]
        payload = payloads.setdefault(
            parent, {"v": 1, "parent": parent, "rows": []})
        countries.setdefault(parent, set()).update(
            payload_countries(contribution))
        for row in contribution["rows"]:
            row_id = row.get("id")
            if not row_id or row_id in row_ids:
                raise ValueError("duplicate or missing row id: %s" % row_id)
            row_ids.add(row_id)
            payload["rows"].append(row)
    # Azerbaijan's Georgian churches belong to the existing Georgian branch.
    # The country module keeps them separate from the local Baku Diocese so
    # this shared branch remains the one owner of the Georgian payload.
    parent = "georgia"
    payload = payloads[parent]
    countries[parent].add("AZ")
    for row in directory_azerbaijan.DIRECT_GEORGIA_ROWS:
        row_id = row.get("id")
        if not row_id or row_id in row_ids:
            raise ValueError("duplicate or missing row id: %s" % row_id)
        if row.get("parent") != parent or row.get("country") != "AZ":
            raise ValueError("%s is not an Azerbaijani Georgian row" % row_id)
        row_ids.add(row_id)
        payload["rows"].append(directory_azerbaijan.clean(row))
    # The OCU vicariate spans Europe and Australia. This module already owns
    # its shared payload, so append the Australian official-directory rows
    # here rather than creating a second branch owner in Oceania.
    parent = "ukraine-ocu"
    payload = payloads[parent]
    countries[parent].add("AU")
    for row in directory_australia.build()[parent]:
        row_id = row.get("id")
        if not row_id or row_id in row_ids:
            raise ValueError("duplicate or missing row id: %s" % row_id)
        if row.get("parent") != parent or row.get("country") != "AU":
            raise ValueError("%s is not an Australian OCU row" % row_id)
        row_ids.add(row_id)
        payload["rows"].append(row)
    for parent, payload in payloads.items():
        scope = sorted(countries[parent])
        if len(scope) == 1:
            payload["country"] = scope[0]
        else:
            payload["countries"] = scope
    row_count = sum(len(p["rows"]) for p in payloads.values())
    if len(payloads) != 243 or row_count != 21136:
        raise ValueError(
            "combined country branches must publish 243 parents and 21136 "
            "rows, got %d parents and %d rows" %
            (len(payloads), row_count))
    return dict(sorted(payloads.items()))


def manifest(payloads=None):
    payloads = payloads or build()
    answer = {}
    for parent, payload in payloads.items():
        entry = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
        }
        if "countries" in payload:
            entry["countries"] = payload["countries"]
        else:
            entry["country"] = payload["country"]
        answer[parent] = entry
    return answer


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in payloads.items():
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    for parent, payload in payloads.items():
        path = output_path(parent)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
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
        print("directory north-west Europe: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Combined country branches: 243 parents, 21136 subordinate bodies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
