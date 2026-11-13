# Plithos traffic snapshots

This directory contains monthly, privacy-safe aggregate traffic snapshots for
plithos.org. It intentionally contains no raw logs or visitor-level data.

Each completed month has two files in `traffic/`:

- `YYYY-MM.json` is the canonical machine-readable record.
- `YYYY-MM.md` is the human-readable interpretation of the same record.

Counts from Cloudflare Web Analytics are estimates after adaptive sampling.
Core Web Vitals are field measurements from real page loads. P75 timing values
are stored in milliseconds; CLS is unitless. Explicit locale paths are a lower
bound on language use.

The collection, privacy and correction rules are in
[`docs/ANALYTICS.md`](../docs/ANALYTICS.md).
