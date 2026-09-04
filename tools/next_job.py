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

TWO LANES MUST NOT PICK THE SAME JOB, so a lane asks by its own slot letter
and gets the Nth job rather than the first. Slots are stable, the ordering is
deterministic, and the queue is derived fresh every time - when a job
finishes it leaves the list and everything below it moves up a place.

    python3 tools/next_job.py                 the whole queue
    python3 tools/next_job.py --slot B        what lane B should do now

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
import importlib.util
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
    a = ap.parse_args()
    q = queue()
    if not a.slot:
        print("%d jobs outstanding\n" % len(q))
        for i, j in enumerate(q):
            print("  %s  %-11s %-9s %6d of %-6d %5d left"
                  % (chr(65 + i) if i < 26 else " ", j["name"], j["kind"],
                     j["have"], j["total"], j["left"]))
        return 0

    i = ord(a.slot.strip().upper()[0]) - 65
    if i < 0 or i >= len(q):
        print("Nothing outstanding for slot %s. %d jobs in the queue; "
              "every one of them is taken by a lower slot." % (a.slot, len(q)))
        return 0
    j = q[i]
    print("SLOT %s: %s %s" % (a.slot.upper(), j["name"], j["kind"]))
    print("%d of %d written, %d remain.\n" % (j["have"], j["total"], j["left"]))
    print("Your batch command:\n\n    %s\n" % command(j))
    if j["kind"] != "interface":
        print("Authority: docs/%s.md" % NAME[j["lang"]].upper())
    return 0


if __name__ == "__main__":
    sys.exit(main())
