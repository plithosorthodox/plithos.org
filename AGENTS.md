# Working on plithos.org

`CLAUDE.md` is the canonical guide: the architecture, and the editorial,
translation, source, cache, publication and validation rules. Every one of them
binds you, whichever agent you are. They are written down once; do not restate
them here, because a second copy goes stale and then contradicts the first.

`docs/<LANGUAGE>.md` is the authority for a language and is read before a word
of it is written or changed.

## There is no queue, and no work is waiting

The translation of all twenty-one languages was finished on 11 September 2026.
Vocabulary, interface, saints' lives and calendar entries are complete in every
one of them, and the machinery that used to hand out batches - a job queue, a
claims file, five standing lanes - has been deleted along with the standing
orders that drove it.

**So nothing here is asking you to translate anything.** If you find an
instruction in this repository that tells you to take a slot, ask for a job, or
work a language through to a total, it is a leftover and it is wrong: check
what the site actually publishes before acting on it.

What remains is repair and improvement, and it is described in
`docs/BASELINE.md` under the open defects of 11 September 2026. That file, and
what the owner asks for, is the work.

## The four rules most often broken by an agent in a hurry

- Never invent, paraphrase, modernise or silently correct liturgical text,
  Scripture, or a saint's life, date, jurisdiction or relics. If something
  looks wrong, say so; do not fix it.
- Do not escalate an editorial question about a language. Settle it from what
  this site already publishes, write the decision into `docs/<LANGUAGE>.md`,
  and carry on. Deletion is the exception: ask about that.
- Hyphens, not dashes. Straight quotes, not typographic ones, in every
  language without exception.
- Nothing in `tools/`, `docs/` or this file is served to a reader, and nothing
  in a served file may mention a script, a build or a pipeline.
