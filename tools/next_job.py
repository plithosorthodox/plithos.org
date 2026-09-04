#!/usr/bin/env python3
"""
What a lane should do next, worked out from the shelf rather than assigned.

Lanes used to be told what to write, one language to a lane, in a trigger
prompt that named it. That goes stale the moment the language finishes: the
lane sits idle until somebody notices, rewrites the prompt, and pokes it. It
also went wrong the other way - a prompt still said SYRIAC LIVES while the
lane had been moved to Urdu, and the lane believed the prompt.

So no lane is told a language any more. Every lane asks this what is next,
and this answers from what the branch actually holds. Nothing to keep in
step, nothing to rewrite when a language finishes, and a lane that wakes up
after a week gets the right answer without being told anything.

TWO LANES MUST NOT PICK THE SAME JOB. Handing out the Nth job by slot letter
is not enough on its own: the queue is derived fresh every time, so the moment
one job finishes everything below it moves up a place and the lane that was on
the fifth job and the lane that was on the fourth are both on the fourth. So a
lane does not take a position, it takes a claim - written into
docs/lane-claims.json and pushed the moment it is made - and it keeps that
claim until the job is done. Slot letters only decide who chooses first.

    python3 tools/next_job.py                 the whole queue
    python3 tools/next_job.py --slot B        what lane B should do now
    python3 tools/next_job.py --claims        who is on what
    python3 tools/next_job.py --slot B --release   give the job back

A claim goes stale after STALE_HOURS and any lane may then take it, so a lane
that dies mid-job does not hold a language hostage.

THE ORDER, and why:

  1. Anything nearly done, fewest remaining first. A language 152 entries
     from a finished vocabulary is worth more than one 3,000 from it: half a
     kind is the worst state to leave anything in, and finishing frees a slot.
  2. Vocabulary. It is what a reader meets first - the names on the Saints
     page - and until it is written that reader is shown English.
  3. The Library and the interface. Small, and the most visible words on the
     site after the names.
  4. Lives, then calendar entries. Deeper in, and a reader who reaches them
     has already been served by the two above.
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

LANGS = ["el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it", "sr",
         "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"]
NAME = {"el": "Greek", "ru": "Russian", "ro": "Romanian", "uk": "Ukrainian",
        "de": "German", "es": "Spanish", "ar": "Arabic", "fr": "French",
        "pt": "Portuguese", "it": "Italian", "sr": "Serbian",
        "ka": "Georgian", "zh": "Chinese", "ja": "Japanese", "ko": "Korean",
        "sw": "Swahili", "hy": "Armenian", "arc": "Syriac", "hi": "Hindi",
        "bn": "Bengali", "ur": "Urdu"}

# kind -> (directory, total, rank, the command a lane runs)
KINDS = {
    "terms":     ("saint_terms", 10632, 1),
    "interface": (None,            342, 2),
    "lives":     ("saint_lives",  1456, 3),
    "entries":   ("saint_info",   1456, 4),
}
NEARLY = 600          # under this many remaining, finish it first
CLAIMS = ROOT / "docs" / "lane-claims.json"
STALE_HOURS = 12      # after this a lane is presumed gone and its job freed


def written(kind, lang):
    """Ask loop.py, which is what the lanes themselves are measured by.

    Counting tools/<dir>/<lang>.py directly looks equivalent and is not: the
    published set is the module plus whatever was written before the module
    existed. That undercount put Greek, Russian and Ukrainian vocabulary in
    this queue as thirteen hundred short apiece when all three have been
    complete for days. One measure, in one place, or the queue sends lanes to
    rewrite what a reader can already read."""
    import loop
    try:
        en, rem = loop.remaining(kind, lang)
        return len(en) - len(rem)
    except Exception:
        return 0


def entries_published():
    """What the calendar actually serves, which is not what the module holds.

    tools/saint_info/<lang>.py carried 1,337 for a dozen languages that the
    calendar has served complete for weeks: the published set is the module
    plus what was written into the pages before the module existed. Counting
    the module invented a backlog of 119 entries in fifteen languages and
    would have sent lanes to write what a reader can already read. The
    builder is the only thing that knows, so it is asked."""
    import re
    import subprocess
    r = subprocess.run([sys.executable, str(TOOLS / "saint_info_i18n.py")],
                       capture_output=True, text=True, timeout=600)
    out = {}
    for m in re.finditer(r"^\s+([a-z]{2,3})\s+(\d+) of (\d+) entries",
                         r.stdout, re.M):
        out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def interface_remaining():
    """One evaluation of the pages, then every language measured against it."""
    import loop_ui
    en = loop_ui.english()
    total = sum(len(v) for v in en.values())
    out = {}
    for lang in LANGS:
        have = loop_ui.carried(lang)
        n = sum(1 for s in en for k in en[s] if (s, k) not in have)
        out[lang] = (total - n, total)
    return out


def queue():
    jobs = []
    iface = interface_remaining()
    pub = entries_published()
    for lang in LANGS:
        for kind, (_, total, rank) in KINDS.items():
            if kind == "interface":
                have, total = iface[lang]
            elif kind == "entries":
                have, total = pub.get(lang, (written(kind, lang), total))
            else:
                have = written(kind, lang)
            left = total - have
            if left <= 0:
                continue
            jobs.append({"lang": lang, "name": NAME[lang], "kind": kind,
                         "have": have, "total": total, "left": left,
                         "rank": rank})
    # nearly-finished first, then by kind, then by how much is left
    jobs.sort(key=lambda j: (0 if j["left"] < NEARLY else 1,
                             j["left"] if j["left"] < NEARLY else j["rank"],
                             j["left"], j["lang"]))
    return jobs


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def read_claims():
    try:
        return json.loads(CLAIMS.read_text())
    except Exception:
        return {}


def fresh_within(c, hours):
    try:
        since = datetime.datetime.fromisoformat(c["since"])
    except Exception:
        return False
    if since.tzinfo is None:
        since = since.replace(tzinfo=datetime.timezone.utc)
    return (now() - since).total_seconds() < hours * 3600


def fresh(c):
    """A claim only speaks for a lane that is still there."""
    return fresh_within(c, STALE_HOURS)


def save_claims(claims, note):
    """Write the claim and push it, because a claim nobody else can see is not
    one. The lanes pull before they ask, so this is what keeps two of them off
    the same file; it is committed on its own so it never waits on a batch."""
    CLAIMS.parent.mkdir(parents=True, exist_ok=True)
    CLAIMS.write_text(json.dumps(claims, indent=2, sort_keys=True) + "\n")
    br = "claude/plithos-org-code-247ox6"
    for cmd in (["git", "add", str(CLAIMS)],
                ["git", "commit", "-m", note],
                ["git", "push", "-u", "origin", br]):
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        if r.returncode and cmd[1] != "commit":
            print("  (the claim is written but not pushed: %s)"
                  % (r.stderr.strip().splitlines() or [""])[-1])
            return


def pick(slot, q):
    """The job this lane is on: the one it already holds if there is work left
    in it, otherwise the best one no other living lane has taken."""
    slot = slot.strip().upper()[0]
    claims = read_claims()
    held = claims.get(slot)
    if held:
        for j in q:
            if j["lang"] == held.get("lang") and j["kind"] == held.get("kind"):
                # A claim is also a sign of life. Refresh it when it is halfway
                # to going stale, and no oftener: a heartbeat on every ask
                # would be four commits a day per lane saying nothing.
                if not fresh_within(held, STALE_HOURS / 2.0):
                    held["since"] = now().replace(microsecond=0).isoformat()
                    claims[slot] = held
                    save_claims(claims, "Lane %s stays on %s %s"
                                % (slot, j["name"], j["kind"]))
                return j, False
    taken = set()
    for s2, c in claims.items():
        if s2 != slot and fresh(c):
            taken.add((c.get("lang"), c.get("kind")))
    for j in q:
        if (j["lang"], j["kind"]) not in taken:
            claims[slot] = {"lang": j["lang"], "kind": j["kind"],
                            "name": j["name"],
                            "since": now().replace(microsecond=0).isoformat()}
            save_claims(claims, "Lane %s takes %s %s"
                        % (slot, j["name"], j["kind"]))
            return j, True
    return None, False


def release(slot):
    slot = slot.strip().upper()[0]
    claims = read_claims()
    held = claims.pop(slot, None)
    if not held:
        print("Lane %s holds nothing." % slot)
        return
    save_claims(claims, "Lane %s gives back %s %s"
                % (slot, held.get("name", held.get("lang")), held.get("kind")))
    print("Lane %s gives back %s %s." % (slot, held.get("name"), held.get("kind")))


def command(j):
    if j["kind"] == "interface":
        return "python3 tools/loop_ui.py %s --next 20 --append batch.txt" % j["lang"]
    n = 40 if j["kind"] == "terms" else 10
    return ("python3 tools/loop.py %s %s --append batch.txt && \\\n"
            "  python3 tools/check_register.py --lang %s && \\\n"
            "  python3 tools/loop.py %s %s --next %d"
            % (j["kind"], j["lang"], j["lang"], j["kind"], j["lang"], n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", help="a lane's slot letter, A onwards")
    ap.add_argument("--claims", action="store_true", help="who is on what")
    ap.add_argument("--release", action="store_true",
                    help="with --slot, give the job back to the queue")
    a = ap.parse_args()

    if a.release:
        if not a.slot:
            print("--release needs --slot")
            return 2
        release(a.slot)
        return 0

    if a.claims:
        c = read_claims()
        if not c:
            print("No lane holds anything.")
            return 0
        for slot in sorted(c):
            h = c[slot]
            print("  %s  %-11s %-9s  since %s%s"
                  % (slot, h.get("name", h.get("lang")), h.get("kind"),
                     h.get("since", "?"), "" if fresh(h) else "   (stale)"))
        return 0

    q = queue()
    if not a.slot:
        held = {(c.get("lang"), c.get("kind")): s2
                for s2, c in read_claims().items() if fresh(c)}
        print("%d jobs outstanding\n" % len(q))
        for i, j in enumerate(q):
            who = held.get((j["lang"], j["kind"]))
            print("  %s  %-11s %-9s %6d of %-6d %5d left%s"
                  % (chr(65 + i) if i < 26 else " ", j["name"], j["kind"],
                     j["have"], j["total"], j["left"],
                     "   lane " + who if who else ""))
        return 0

    j, taken = pick(a.slot, q)
    if j is None:
        print("Nothing outstanding for lane %s. Every job in the queue is "
              "held by another lane." % a.slot.strip().upper()[0])
        return 0
    print("LANE %s: %s %s%s" % (a.slot.strip().upper()[0], j["name"], j["kind"],
                                "   (newly taken)" if taken else "   (yours already)"))
    print("%d of %d written, %d remain.\n" % (j["have"], j["total"], j["left"]))
    print("Your batch command:\n\n    %s\n" % command(j))
    if j["kind"] != "interface":
        print("Authority: docs/%s.md" % NAME[j["lang"]].upper())
    print("When this job reaches its total, the claim clears itself: ask "
          "again and you will be given the next one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
