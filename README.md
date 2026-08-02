# plithos.org

Source for the [plithos.org](https://plithos.org) website.

## Status

Repository scaffolding only. The site itself — currently a set of plain HTML
files — has not been added yet.

## Stack

Plain HTML, CSS, and JavaScript. No build step and no dependencies, so the
files in this repository are exactly what gets served.

## Local preview

No install required. From the repository root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Opening an `.html` file directly with `file://` mostly works, but a local
server is closer to production and avoids path and CORS surprises.

## Repository layout

```
.claude/settings.json   Claude Code permissions for this repo
CLAUDE.md               Project context and conventions for Claude Code
.gitignore
```

Site files will be added at the root.

## Working with Claude Code

`CLAUDE.md` is read automatically at the start of every Claude Code session in
this repo — it is the place to record project context, conventions, and
anything Claude should not do. Keep it current as the site grows.
