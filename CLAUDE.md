# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

The code for **plithos.org**, the website for Plithos Orthodox.

> **Status: scaffolding.** The site itself has not been committed yet. The
> existing site is plain HTML and will be added to this repo shortly. Once it
> lands, update the "Layout", "Commands", and "Conventions" sections below to
> match what's actually here — the placeholders are marked `TBD`.

## Stack

- Plain HTML / CSS / JavaScript. No build step, no package manager, no
  framework.
- Because there is no build, **what is in the repo is what ships**. Edits to
  `.html` files are the deployed artifact.

## Layout

TBD — fill in once the site is committed. Expected shape:

```
/                 # page HTML lives at the root
  index.html
  <page>.html
/assets or /css   # stylesheets
/js               # scripts
/images           # media
```

## Commands

There is no toolchain yet, so there is nothing to install, build, or test.

To preview the site locally:

```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

TBD — replace if a build tool, linter, or test runner is added later.

## Conventions

Until the real site is committed and its conventions can be read off the code,
default to these:

- **Match the surrounding file.** Indentation, quote style, class naming, and
  markup structure should look like the page you are editing, not like a
  general best practice.
- **Semantic HTML.** Use `<header>`, `<nav>`, `<main>`, `<section>`,
  `<footer>`, and real heading levels rather than `<div>` soup.
- **Accessibility is not optional.** Every `<img>` needs meaningful `alt`;
  interactive elements must be reachable and operable by keyboard; keep colour
  contrast at WCAG AA or better.
- **No new dependencies without asking.** Do not add a framework, a build
  step, a CDN `<script>` tag, or a web font without checking first. Keeping
  this site dependency-free is a deliberate choice.
- **Shared markup is duplicated across pages.** With no templating layer, a
  change to the header, nav, or footer has to be applied to *every* page.
  When editing shared chrome, grep for it and update all occurrences.

## Content

This is the website of an Orthodox Christian organisation. Content may include
liturgical text, scripture, saints' names, feast days, and transliterated Greek
or Church Slavonic.

- **Do not paraphrase, modernise, correct, or invent liturgical or scriptural
  text.** Reproduce it exactly as given. If something looks like an error, ask
  rather than "fixing" it.
- Preserve diacritics and non-ASCII characters exactly; make sure pages declare
  `<meta charset="utf-8">`.
- Keep proper nouns, titles, and spellings as the maintainer writes them.

## Working agreements

- Ask before doing anything destructive or hard to reverse — deleting pages,
  restructuring directories, rewriting git history, or changing DNS/deploy
  configuration.
- Do not commit or push unless asked.
- Report honestly. If something is untested or partly done, say so.
