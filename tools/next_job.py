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
import os
import re
import subprocess
import sys
import tempfile
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
# A second lane may join a language when nothing else is outstanding, working
# the remaining list from the far end. It is only worth doing while there is
# room between them: below this many remaining the two ends are close enough
# that both could be offered the same saint in one cycle, so the job goes back
# to one lane and the spare waits for the next thing to open.
SHARE_FLOOR = 60


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
        entry_count = pub[lang] if lang in pub else (written("info", lang),
                                                     KINDS["entries"][1])
        counts = {
            "terms": (written("terms", lang), KINDS["terms"][1]),
            "interface": iface[lang],
            "lives": (written("lives", lang), KINDS["lives"][1]),
            "entries": entry_count,
        }
        # Vocabulary gates every later lane. Once it is complete, interface
        # and lives may proceed; entries wait for lives to be complete too.
        if counts["terms"][0] < counts["terms"][1]:
            eligible = ("terms",)
        else:
            eligible = ("interface", "lives")
            if counts["lives"][0] >= counts["lives"][1]:
                eligible += ("entries",)
        for kind in eligible:
            _, _, rank = KINDS[kind]
            have, total = counts[kind]
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


SLOT = re.compile(r"^[A-Z0-9][A-Z0-9-]{0,15}$")


def slot_name(raw):
    """A worker's name in the claims file.

    It used to be `raw.strip().upper()[0]` - the first letter and nothing else.
    That was safe while the only workers were five lanes called A to E, and it
    is a trap now that they are not: a worker calling itself CODEX-1 would have
    been filed under C and taken lane C's claim out from under it. The whole
    name is the key."""
    name = " ".join(str(raw).split()).upper().replace(" ", "-")
    if not SLOT.match(name):
        raise SystemExit("a slot name is letters, digits and hyphens, "
                         "sixteen at most: %r" % raw)
    return name


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def read_claims():
    try:
        return json.loads(CLAIMS.read_text())
    except Exception:
        return {}


class ClaimError(RuntimeError):
    pass


def integration_branch():
    """The shared branch, independent of the worker's checked-out branch."""
    configured = os.environ.get("PLITHOS_INTEGRATION_BRANCH")
    if configured:
        return configured.removeprefix("refs/heads/").removeprefix("origin/")
    r = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip().startswith("origin/"):
        return r.stdout.strip()[len("origin/"):]
    r = subprocess.run(["git", "branch", "--show-current"], cwd=str(ROOT),
                       capture_output=True, text=True)
    if r.returncode or not r.stdout.strip():
        raise ClaimError("cannot determine the shared integration branch")
    return r.stdout.strip()


def _git(args, input_text=None, env=None):
    r = subprocess.run(["git"] + args, cwd=str(ROOT), input=input_text,
                       capture_output=True, text=True, env=env)
    if r.returncode:
        raise ClaimError((r.stderr.strip().splitlines() or r.stdout.strip().splitlines()
                          or ["git command failed"])[-1])
    return r.stdout.strip()


def remote_claims(ref):
    try:
        return json.loads(_git(["show", ref + ":docs/lane-claims.json"]))
    except ClaimError:
        return {}


def synchronized_claims():
    branch = integration_branch()
    _git(["fetch", "origin", branch])
    return remote_claims("refs/remotes/origin/" + branch)


def fresh_within(c, hours):
    try:
        since = datetime.datetime.fromisoformat(c["since"])
    except Exception:
        return False
    if since.tzinfo is None:
        since = since.replace(tzinfo=datetime.timezone.utc)
    return (now() - since).total_seconds() < hours * 3600


_LAST_WORK = {}


def last_work(kind, lang):
    """When this language's file last changed on the shared branch.

    A lane refreshes its claim only when it asks the queue, and a lane deep in
    a batch loop does not ask for hours. On 5 September four lanes were within
    an hour of being declared gone while committing work every few minutes,
    because the only evidence anyone looked at was when they had last spoken.
    Work landing on the branch is better evidence than that, and it is the
    evidence a worker cannot forge by saying nothing.
    """
    directory = (KINDS.get(kind) or (None,))[0]
    if not directory:
        return None
    key = (directory, lang)
    if key not in _LAST_WORK:
        path = "tools/%s/%s.py" % (directory, lang)
        try:
            branch = integration_branch()
            _git(["fetch", "origin", branch])
            stamp = _git(["log", "-1", "--format=%cI",
                          "refs/remotes/origin/" + branch, "--", path])
        except Exception:
            stamp = ""
        try:
            when = datetime.datetime.fromisoformat(stamp) if stamp else None
        except ValueError:
            when = None
        if when is not None and when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        _LAST_WORK[key] = when
    return _LAST_WORK[key]


def fresh(c):
    """A claim only speaks for a lane that is still there.

    Still there means still working, not still talking. Either the lane
    refreshed its claim recently, or its language has commits on the branch
    recently; a lane doing neither for half a day really has gone.
    """
    if fresh_within(c, STALE_HOURS):
        return True
    when = last_work(c.get("kind"), c.get("lang"))
    if when is None:
        return False
    return (now() - when).total_seconds() < STALE_HOURS * 3600


def save_claim(slot, held, note, retries=3):
    """Atomically publish one slot on the shared branch and confirm it there."""
    branch = integration_branch()
    remote_ref = "refs/remotes/origin/" + branch
    for attempt in range(retries):
        _git(["fetch", "origin", branch])
        base = _git(["rev-parse", remote_ref])
        claims = remote_claims(remote_ref)
        if held is None:
            claims.pop(slot, None)
        else:
            wanted = (held.get("lang"), held.get("kind"))
            others = [c for s, c in claims.items()
                      if s != slot and fresh(c)
                      and (c.get("lang"), c.get("kind")) == wanted]
            # One lane to a job, except for a deliberate share: a second lane
            # may join from the far end of the remaining list when there is
            # nothing else outstanding. Two from the front would write the
            # same saints; a third has nowhere to stand at all.
            if others and not (held.get("from_end")
                               and not any(c.get("from_end") for c in others)):
                return False
            claims[slot] = held
        content = json.dumps(claims, indent=2, sort_keys=True) + "\n"
        with tempfile.TemporaryDirectory(prefix="plithos-claim-") as td:
            path = Path(td) / "claims.json"
            path.write_text(content, encoding="utf-8")
            blob = _git(["hash-object", "-w", str(path)])
            index = str(Path(td) / "index")
            env = dict(os.environ, GIT_INDEX_FILE=index)
            _git(["read-tree", base], env=env)
            _git(["update-index", "--add", "--cacheinfo", "100644", blob,
                  "docs/lane-claims.json"], env=env)
            tree = _git(["write-tree"], env=env)
            commit = _git(["-c", "user.name=Plithos lane coordinator",
                           "-c", "user.email=coordination@plithos.org",
                           "commit-tree", tree, "-p", base, "-m", note])
        pushed = subprocess.run(
            ["git", "push", "origin", "%s:refs/heads/%s" % (commit, branch)],
            cwd=str(ROOT), capture_output=True, text=True)
        if pushed.returncode:
            if attempt + 1 < retries:
                continue
            raise ClaimError("claim push rejected after synchronization: %s" %
                             ((pushed.stderr.strip().splitlines() or [""])[-1]))
        _git(["fetch", "origin", branch])
        if _git(["rev-parse", remote_ref]) == commit \
                and remote_claims(remote_ref) == claims:
            return True
        if attempt + 1 == retries:
            raise ClaimError("claim was pushed but not confirmed on the shared branch")
    return False


def pick(slot, q):
    """The job this lane is on: the one it already holds if there is work left
    in it, otherwise the best one no other living lane has taken."""
    slot = slot_name(slot)
    claims = synchronized_claims()
    held = claims.get(slot)
    if held:
        for j in q:
            if j["lang"] == held.get("lang") and j["kind"] == held.get("kind"):
                # A claim is also a sign of life. Refresh it when it is halfway
                # to going stale, and no oftener: a heartbeat on every ask
                # would be four commits a day per lane saying nothing.
                if not fresh_within(held, STALE_HOURS / 2.0):
                    held["since"] = now().replace(microsecond=0).isoformat()
                    if not save_claim(slot, held, "Lane %s stays on %s %s"
                                      % (slot, j["name"], j["kind"])):
                        raise ClaimError("the existing claim could not be refreshed")
                return j, False
    taken = set()
    for s2, c in claims.items():
        if s2 != slot and fresh(c):
            taken.add((c.get("lang"), c.get("kind")))
    for j in q:
        if (j["lang"], j["kind"]) not in taken:
            held = {"lang": j["lang"], "kind": j["kind"], "name": j["name"],
                    "since": now().replace(microsecond=0).isoformat()}
            if save_claim(slot, held, "Lane %s takes %s %s"
                          % (slot, j["name"], j["kind"])):
                return j, True

    # Nothing unheld. Rather than stand idle, join the job with the most left
    # in it and work the remaining list from the other end. Only a job one
    # lane holds, and only while there is room between the two ends.
    shared = {(c.get("lang"), c.get("kind")) for s2, c in claims.items()
              if s2 != slot and fresh(c) and c.get("from_end")}
    for j in sorted(q, key=lambda j: -j["left"]):
        if j["left"] < SHARE_FLOOR:
            continue
        if (j["lang"], j["kind"]) in shared:
            continue          # already has two lanes on it
        held = {"lang": j["lang"], "kind": j["kind"], "name": j["name"],
                "from_end": True,
                "since": now().replace(microsecond=0).isoformat()}
        if save_claim(slot, held, "Lane %s joins %s %s from the other end"
                      % (slot, j["name"], j["kind"])):
            return j, True
    return None, False


def release(slot):
    slot = slot_name(slot)
    claims = synchronized_claims()
    held = claims.pop(slot, None)
    if not held:
        print("Lane %s holds nothing." % slot)
        return
    save_claim(slot, None, "Lane %s gives back %s %s"
               % (slot, held.get("name", held.get("lang")), held.get("kind")))
    print("Lane %s gives back %s %s." % (slot, held.get("name"), held.get("kind")))


def command(j, from_end=False):
    if j["kind"] == "interface":
        return "python3 tools/loop_ui.py %s --next 20 --append batch.txt" % j["lang"]
    n = 40 if j["kind"] == "terms" else 10
    loop_kind = "info" if j["kind"] == "entries" else j["kind"]
    tail = " --from-end" if from_end else ""
    return ("python3 tools/loop.py %s %s --append batch.txt && \\\n"
            "  python3 tools/check_register.py --lang %s && \\\n"
            "  python3 tools/loop.py %s %s --next %d%s"
            % (loop_kind, j["lang"], j["lang"], loop_kind, j["lang"], n, tail))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", help="this worker's name: A-E are the "
                    "standing lanes, CODEX-1 onwards are Codex's")
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
        c = synchronized_claims()
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
                for s2, c in synchronized_claims().items() if fresh(c)}
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
              "held by another worker." % slot_name(a.slot))
        return 0
    from_end = bool(synchronized_claims().get(slot_name(a.slot), {}).get("from_end"))
    print("LANE %s: %s %s%s" % (slot_name(a.slot), j["name"], j["kind"],
                                "   (newly taken)" if taken else "   (yours already)"))
    print("%d of %d written, %d remain.\n" % (j["have"], j["total"], j["left"]))
    if from_end:
        print("You are the second lane on this language. Another lane is working\n"
              "the same list from the front; you work it from the back. Your batch\n"
              "command already says so - keep --from-end on every call, and do not\n"
              "reach for the front of the list even if it looks unwritten.\n")
    print("Your batch command:\n\n    %s\n" % command(j, from_end))
    if j["kind"] != "interface":
        print("Authority: docs/%s.md" % NAME[j["lang"]].upper())
    print("When this job reaches its total, the claim clears itself: ask "
          "again and you will be given the next one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
