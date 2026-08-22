# The loop

How a language gets written without stopping.

## Why this file exists

The saints' lives and the calendar entries were written in long unbroken
runs - a hundred and fifty-odd batches, no stops. The vocabulary and the
grammar were not, and the difference was never editorial. It was that the
machinery for the first two was three throwaway scripts in a temp directory,
and the machinery for the other two did not exist. Nothing could inherit
what was never a tool in the repository. `tools/loop.py` is that machinery,
written down.

## The shape

Three things, and all three are needed. Take any one away and the run stops
every few batches.

1. **A stable queue.** `remaining()` is
   `[k for k in sorted(english) if k not in written]` - sorted, so the same
   command returns the same next ten tomorrow, on another machine, after the
   container is gone. There is no freeze file to lose. What is already
   written is read from *both* places it can live, which for the calendar
   means the module in `tools/saint_info/` and `SAINT_INFO_I18N` inside
   `index.html`. Reading one of the two re-queues work that is finished:
   that bug was live, and it would have had a hundred and forty-six German
   entries translated a second time.

2. **An appender keyed off that queue.** Blocks are matched against
   `--next` in order, so a key is never retyped and so cannot be
   misspelled into a phrase the index does not show. The guards are worth
   more than the typing they save: a placeholder left in, a stray character
   the language does not use, the wrong number of lines in a block, more
   blocks than there are entries left. Any one of them fails before the
   file is touched. After the write the module is imported again, and if it
   does not parse the backup is restored.

3. **One invocation that appends and prints the next batch.** This is the
   part that actually removes the stops. Append, check, commit, push *and*
   print the next ten, all in a single command, so no batch ever waits on
   reading the result of the batch before it.

## Running it

    python3 tools/loop.py info de --status
    python3 tools/loop.py info de --next 10

Write the blocks, separated by lines containing only `@@@`, then:

    python3 tools/loop.py info de --append batch.txt && \
      python3 tools/saint_info_i18n.py --check && \
      python3 tools/loop.py info de --next 10

Beginning a language:

    python3 tools/loop.py terms sr --start Serbian

`lives`, `info` and `terms` are the three kinds. They differ only in which
directory they write to and how many lines a block holds.

## Three lanes at once

The three kinds write to three different directories and never touch the same
file, so they can be written at the same time by three sessions on one branch.
Serbian was done that way in a day: the lives, the calendar entries and the
vocabulary each in a session of its own, all pushing to
`claude/plithos-org-code-247ox6`, none of them waiting on the others and none
of them asking anything.

A lane is created, not talked to. It is given one standing instruction that
contains everything it needs, and it runs to the end of the queue on its own.
There is no follow-up message, and that is the whole reason nothing comes back
to be confirmed. When a lane finishes it goes idle and is not reachable again;
more work means another lane, not the same one woken up.

    mcp__Claude_Code_Remote__create_session
      title            "Spanish: the vocabulary"
      tags             ["plithos-loop", "spanish"]
      permission_mode  "auto"
      source_url       "https://github.com/plithosorthodox/plithos.org"
      source_revision  "claude/plithos-org-code-247ox6"
      prompt           the standing instruction

**Name the source and the revision.** They look redundant - a new lane inherits
the parent's repository, and for a while it did. Then creation began refusing,
first as "the service is temporarily unavailable" and then, when the same
sessions were started by hand, as "the requested branch or commit was not found
in the repository". The branch was there the whole time: it is the only branch
this repository has and it is also its default, and the GitHub API said so when
asked. What was missing was the lane saying which revision it wanted. Passing
the two explicitly worked on the first attempt after ten failures over two
hours, and it costs one line to never lose two hours to it again.

What the standing instruction has to carry, because the lane starts from
nothing and cannot ask:

- **What to read first.** `CLAUDE.md` and this file, then the register notes
  of two languages already written.
- **Run to completion, in those words.** That a batch has finished is not a
  reason to report, and not a reason to ask whether to go on. Name the three
  things that may stop it: a failed check, an editorial fork precedent cannot
  settle, the end of context.
- **The one command**, written out, with `--next` on the end of it.
- **The branch, and what to do when the push is rejected.** `git pull
  --rebase` and push again. The lanes share a branch and never share a file,
  so a rejected push is only that the branch moved.
- **The files it may touch, and `--check` only.** A lane must never run a
  builder with `--write` or `tools/stamp_build.py`: `saint_info_i18n.py
  --write` edits `index.html`, which every lane would then be editing at once.
  Publishing belongs to one session, after the lanes are done.
- **Not to open a pull request.**

What it costs is worth knowing before three are started. Serbian, at the
prices of the day: the lives $27, the calendar entries $79, the vocabulary
$134. The vocabulary is seven times the size of the other two and is the long
pole every time.

## Finish a language before beginning another

Spanish and French were left with their lives written and neither their
vocabulary nor their calendar entries, which is a third of a language each and
is how the count came to say eight languages of lives and six of everything
else. `docs/ROMANIAN.md` states the rule - one language at a time, completely,
before the next is begun - and it is stated there rather than here because
that is where it was first broken.

The order within a language is vocabulary, then lives, then calendar entries,
and that is not a preference. `check_register.py --scaffold` derives a
language's rank patterns from its own terms table and refuses a language that
has not got one, so lives written before vocabulary are lives written without
the check that vocabulary would have supplied.

## Vocabulary before grammar

`tools/saint_terms/<lang>.py` may be written entirely as `TEXT`. `PARTS`
and `expand()` are optional - `build_saint_terms.py` calls `expand()` only
`if hasattr(mod, "expand")`. This matters more than it looks. Deciding, for
each of ten thousand phrases, whether it is an atom, a compound or a title
is a judgment per phrase, and a judgment per phrase is a stop per phrase.
Write them all out; factor the repeated lands into `PARTS` afterwards, or
never.

The grammar is drawn from the vocabulary, not written beside it.
`tools/check_register.py --scaffold --lang <lang>` reads the language's own
terms table and derives the `ranks` and `monastic` patterns from the rank
words it already renders. What is left is two editorial decisions - the
bare word for holy, and whether the language forbids it before a name at
all - and the scaffold marks both. It refuses to scaffold a language whose
terms table does not exist yet, which is the ordering above, enforced.

    python3 tools/check_register.py --scaffold --lang sr
    python3 tools/check_register.py --lang de --review 40

`--review` prints the soft findings in stable order: a saint given some
other real rank than his order would suggest, which a calendar may
legitimately do and a script may not judge.

## What still stops the loop

A failed check, an editorial fork that precedent cannot settle, or the end
of context. A batch ending is not one of them.

## If it stops anyway

Go and find out why. The stopping during the German vocabulary was reported
several times and answered several times with an explanation of why that
kind of work was different - the judgment per phrase, the atom against the
compound. The explanation was wrong, and the true answer cost one command:

    git ls-files | grep -E "appde|appinfo|todo"

Nothing. The machinery that drove the runs which did not stop had never been
in the repository at all. A report that the loop is stopping is evidence
about a defect, not a misunderstanding to be corrected. The sentence "this
kind of work inherently needs a stop" is the signal to go and look at why
the other loop did not, not the conclusion.
