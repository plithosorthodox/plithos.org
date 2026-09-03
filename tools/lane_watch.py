#!/usr/bin/env python3
"""
Decide what to do with each standing lane, from what the lanes report.

A lane is a session of its own working one language. It stops for two reasons
that look identical from outside - it has spent the five-hour allowance, or it
has quietly stalled - and the remedy is opposite: the first must be left alone
until the window rolls over, the second must be poked at once. Poking a lane
that is out of allowance does nothing except mark it failed again; waiting on a
lane that has merely stalled costs however long it is until somebody looks.

Six lanes sat dead for two hours and forty minutes because the check-in ran on
a fixed schedule and the window had rolled over eleven minutes after it.

What each session reports is enough to tell the two apart:

    rate_limit_info.status   rejected          the allowance is spent
                             allowed_warning   nearly spent
                             allowed           there is room
    rate_limit_info.resetsAt when the window rolls over, as a unix time
    session_status           RUNNING IDLE REQUIRES_ACTION

So:

    rejected, and the window has not yet rolled over   PAUSED  - leave it, and
                                                       come back at resetsAt
    rejected, but the window has rolled over           READY   - the record is
                                                       stale; fire it
    allowed_warning                                    SPENDING - leave it
                                                       running, start nothing
    allowed and RUNNING                                WORKING - leave it
    allowed and IDLE                                   STALLED - fire it bare
    REQUIRES_ACTION                                    BLOCKED - read what it
                                                       is asking to run

And the resume is a time, not a guess: the earliest resetsAt among the paused
lanes, plus a minute's grace, printed as the RFC3339 stamp to wake at. Nothing
is polled and no lane is poked while it cannot answer.

The session records come from the remote session tool, which this cannot call;
save them and pass the file.

    python3 tools/lane_watch.py lanes.json
    python3 tools/lane_watch.py lanes.json --at 2026-09-03T02:40:00Z
"""
import argparse
import datetime as dt
import json
import re
import sys

GRACE = 60          # a minute past the reset, so the window is certainly open


def records(raw):
    """Every {"ccr": {...}} in the text, however it was pasted together."""
    out, i = [], 0
    while True:
        j = raw.find('"ccr"', i)
        if j < 0:
            break
        k = raw.rfind("{", 0, j)
        dec = json.JSONDecoder()
        try:
            obj, end = dec.raw_decode(raw[k:])
        except ValueError:
            i = j + 5
            continue
        out.append(obj.get("ccr", obj))
        i = k + end
    if not out:
        try:
            o = json.loads(raw)
            out = o if isinstance(o, list) else [o.get("ccr", o)]
        except ValueError:
            pass
    return out


def rate(r):
    ex = r.get("external_metadata") or {}
    return ex.get("rate_limit_info") or {}


def verdict(r, now):
    st = (r.get("session_status") or "").replace("SESSION_STATUS_", "")
    rl = rate(r)
    status = rl.get("status") or "unknown"
    resets = rl.get("resetsAt")
    if st == "REQUIRES_ACTION":
        return "BLOCKED", "waiting on a permission prompt", resets
    if status == "rejected":
        if resets and resets <= now:
            return "READY", "the window rolled over; the record is stale", resets
        return "PAUSED", "the allowance is spent", resets
    if status == "allowed_warning":
        return "SPENDING", "nearly spent; start nothing new", resets
    if st == "RUNNING":
        return "WORKING", "", resets
    if st == "IDLE":
        return "STALLED", "idle with allowance left", resets
    return "UNKNOWN", st.lower() or "no status", resets


def pending(r):
    ex = r.get("external_metadata") or {}
    p = ex.get("pending_action") or {}
    cmd = (p.get("input") or {}).get("command") or p.get("raw_command") or ""
    return re.sub(r"\s+", " ", cmd).strip()


def stamp(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="the saved session records; - for stdin")
    ap.add_argument("--at", help="treat this RFC3339 time as now, for checking")
    a = ap.parse_args()

    raw = sys.stdin.read() if (not a.file or a.file == "-") \
        else open(a.file, encoding="utf-8").read()
    rs = records(raw)
    if not rs:
        raise SystemExit("no session records in that")

    if a.at:
        now = int(dt.datetime.strptime(a.at, "%Y-%m-%dT%H:%M:%SZ")
                  .replace(tzinfo=dt.timezone.utc).timestamp())
    else:
        now = int(dt.datetime.now(dt.timezone.utc).timestamp())
    print("as at %s\n" % stamp(now))

    fire, paused = [], []
    for r in rs:
        v, why, resets = verdict(r, now)
        title = (r.get("title") or "")[:34]
        when = stamp(resets) if resets else "-"
        print("%-8s %-34s %-21s %s" % (v, title, when, why))
        print("         %s" % r.get("id"))
        if v == "BLOCKED":
            c = pending(r)
            if c:
                print("         asking to run: %s" % c[:150])
        if v in ("READY", "STALLED"):
            fire.append((r.get("id"), title))
        if v == "PAUSED" and resets:
            paused.append((resets, r.get("id"), title))

    print()
    if fire:
        print("fire these, bare - a note sends the work somewhere that is not the lane:")
        for i, t in fire:
            print("   %s   %s" % (i, t))
    else:
        print("nothing to fire")

    if paused:
        paused.sort()
        when = paused[0][0] + GRACE
        print("\n%d lane(s) are out of allowance. The first window rolls over at %s."
              % (len(paused), stamp(paused[0][0])))
        print("come back at %s" % stamp(when))
        for t, i, ttl in paused:
            print("   %s  %s   %s" % (stamp(t), i, ttl))
    else:
        print("\nno lane is out of allowance; nothing to come back for")
    return 0


if __name__ == "__main__":
    sys.exit(main())
