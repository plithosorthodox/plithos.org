# Codex repository guidance

Read and follow `CLAUDE.md` before making changes. It is the canonical guide
to Plithos' architecture and its editorial, translation, source, batching,
cache, publication, and validation rules; Codex must preserve all of them.

For translation-lane work, also read `docs/LOOP.md` completely and the named
language's `docs/<LANGUAGE>.md` authority before taking a job. Use the existing
appenders and checks exactly as documented. Never invent, paraphrase,
modernise, or silently correct reader-facing, liturgical, scriptural, or
hagiographic text. Preserve source provenance, native script, diacritics,
numbers, dates, centuries, verse references, and source references.

Coordination-only work must not change reader-facing content or generated
published bundles. Do not run a builder with `--write`, stamp a build, deploy,
or merge a pull request unless the task explicitly authorizes that action.
