# Handoff

**The branch is the record.** What was done and why is in the commit messages,
what is left is in `python3 tools/next_job.py`, and who is on what is in
`docs/lane-claims.json`. None of that belongs here.

This file carries only what those cannot say: a decision that binds the next
worker, a defect found and not yet fixed, and a thing that was got wrong once
and must not be got wrong again. If a reader of the git log would already know
it, leave it out.

Newest first. One heading per entry, dated, signed with the worker. Delete an
entry when it stops being true - a defect that has been fixed is history, and
history is in the log.

---

## A quoted verse takes the edition's spelling, not the house spelling

Found 2026-09-04, CLAUDE-LEAD. Open: thirty Hindi lives carry it, unedited
pending the owner's decision.

The Hindi lives in `tools/saint_lives/hi.py` quote the New Testament from
`data/bible.v4.hi.b64` and change it on the way. Three of the first four
quotations checked differ. Two distinct causes, and the distinction is the
point of this entry.

**The nasal mark is the site's own house spelling and it must not reach a
quoted verse.** Hindi here writes chandrabindu - the prayers 266 times, the
saints' vocabulary 1,009 times - and the edition in the bundle uses anusvara
throughout and never the chandrabindu. So a life that writes `जाएँ` where the
verse reads `जाएं` is being consistent with the site and inconsistent with the
source, and CLAUDE.md settles which one wins: reproduce sources exactly. This
generalises past Hindi. **Wherever a language's house orthography differs from
the edition the site publishes, the quotation keeps the edition's form.** Do
not spell a verse the way the surrounding prose is spelled.

**The danda is a real question and is not settled.** `docs/HINDI.md` rules from
counts that Hindi prose here ends in `।`, and it is right about prose. The
lives apply it to the close of a quoted verse where the published text has a
full stop or a comma. Whether a language doc governs punctuation inside a
sentence the site did not write has not been decided. Until it is: keep the
published punctuation inside the quotation marks, put your own outside them.

**Truncating a verse to the clause needed is not a fault** and needs no note.

Nothing here is fixed. Editing a life that is already appended changes
reader-facing scriptural text, and that is the owner's to authorize.

---

## Codex branches, and why "unmerged" cannot be trusted here

Integrated, and needing no further attention:

    codex/coordination-safety   merged 2026-09-04, in part. Its checks were
                                repaired first and are NOT wired into
                                loop.append(); see the entry below.

Awaiting review: none.

**`git branch -r --no-merged` will not tell you this.** Everyone here pulls with
`--rebase`, which flattens a merge commit, so a topic branch stops being an
ancestor the moment anyone rebases after the merge - and then reads as unmerged
for ever, however thoroughly its content was taken. `codex/coordination-safety`
is listed by that command right now and every file of it is on the branch.

So this list is the record, kept by hand, and it is short enough to keep. When
you merge a topic branch, add a line here in the same commit. If you want the
merge to survive as a merge, push it before you pull again.

## 2026-09-04 - A run of Arabic place names sits one key out of step

Arabic is published as a complete vocabulary and part of it is misaligned. Six
consecutive keys each hold the rendering that belongs to the key after them:

    Belgorod                                 has  Belgorod, Russia
    Belgorod (Akkerman), Black Sea coast     has  Belgorod, Russia; incorrupt, 1991
    Belgorod, Russia                         has  Belgrade
    Belgorod, Russia; incorrupt ... in 1991  has  Belgrade, Serbia
    Belgrade                                 has  Belozersk
    Belgrade, Serbia                         has  the lands of Belozersk and Mozhaysk

**The extent of the run is not known and is not guessed at here.** It is at
least these six and it continues into the Belozersk keys. What is known is that
it is local rather than corpus-wide: of the 765 Arabic phrases carrying a
number, 743 carry the right one, which a shifted vocabulary could not do.

Two ways of sizing it were tried and neither is sound. Comparing numbers finds
only keys that carry one, and Arabic spells most of them in words. Comparing a
place name against the Arabic form the corpus uses elsewhere breaks on the
article and the prefixed prepositions - الأونيغا for أونيغا, للقديس for
القديس - and reported 565 keys, every one of them right. Do not repeat either
and do not report a figure from them.

Repairing it wants someone reading Arabic, with `docs/ARABIC.md` in hand. The
queue cannot hand this out: it knows what is unwritten, not what is wrong.

## 2026-09-04 - Check a rendering against the name it stands under

Two defects of one shape were found in a day. Ten Syriac lives stood under the
wrong apostles because a batch was appended twice; a run of Arabic place names
stands one key out of step. Nothing failed in either case - the language was
sound, the count was right, and the register check passed, because it reads the
opening of a life for its honorific and not for whose life it is.

An appender guards the rendering. Nothing guarded the pairing. Comparing each
rendering against the name the index prints for it is what found both, and it
is worth doing to a batch before it is pushed. `docs/SYRIAC.md` carries the
check as lane E wrote it.

## 2026-09-04 - The checks report; they do not stop a lane

`tools/translation_checks.py` holds the deterministic guards - blank, marker
left behind, English left standing, native script, numbers, truncation,
duplicate. They are called from `tools/check_translations.py`, which reports,
and deliberately **not** from `loop.append()`, which would stop a lane.

They were wired into `loop.append()` when they were written. Run against the
corpus already published and accepted they raised 8,268 errors, nearly all of
them wrong: "todo" is Spanish for "all"; Arabic writes its numerals and Chinese
writes a year in characters; German writes Prophet for Prophet; and one saint
under two spellings shares one life. Repaired, they raise 256, of which the ten
Syriac duplicates are real and the rest are Arabic and want a reading.

Before wiring any check into the write path, run it over what is already
published. A check that has never been shown to be quiet on accepted work is
not a check, it is a stoppage waiting for a shift to begin. - Claude, lane parent

## 2026-09-04 - A slot name is the whole name

`next_job.py --slot` used to take the first letter and discard the rest, which
was safe while the only workers were lanes A to E. A worker calling itself
CODEX-1 would have been filed under C and taken lane C's claim. Fixed; the name
is now letters, digits and hyphens, and is used whole. - Claude, lane parent
