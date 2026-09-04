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

## 2026-09-04 - Twenty Syriac lives are ten lives written twice

Positions 60 to 69 of the lives index carry the text of positions 50 to 59.
Sosthenes has been given Matthias' life, John the Theologian has Silas', Luke
has Silvanus'. A batch of ten was appended twice, so the second ten went in
against the wrong keys.

The first ten are right and hold their own text. The second ten are wrong:

    Apostle Sosthenes of the Seventy          Apostle Trophimus of the Seventy
    Apostle Tertius of the Seventy            Apostle and Evangelist John the Theologian
    Apostle Thaddeus of the Seventy           Apostle and Evangelist Luke
    Apostle Timon the Deacon of the Seventy   Apostle and Evangelist Luke of the Seventy
    Apostle Timothy of the Seventy            Apostle Titus of the Seventy and Bishop of Crete

They cannot be corrected in place - writing a Syriac life to cover the gap
would be inventing hagiography, which is the worse fault. They have to be
removed so the loop serves them again, and that is a deletion, so it is asked
about first. Until then Syriac lives are published with ten saints carrying
another saint's life.

`python3 tools/check_translations.py` reports them. - Claude, lane parent

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
