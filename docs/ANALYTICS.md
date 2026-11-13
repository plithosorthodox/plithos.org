# Traffic snapshot policy

Plithos keeps one aggregate traffic snapshot for each completed UTC calendar
month. The snapshots preserve the long-term trend after the analytics provider
ages or samples its own history. They are evidence for product and interface
decisions, not a visitor-tracking archive.

## Schedule and source

Collect the previous full month on or after the second day of each new month.
The source is Cloudflare Web Analytics with known bots excluded and the host
restricted to `plithos.org`:

- `rumPageloadEventsAdaptiveGroups` for pageviews, visits and dimensions.
- `rumWebVitalsEventsAdaptiveGroups` for field performance.
- The deployed `version.json` build value and, when it can be established, the
  source commit that produced it.

Cloudflare Web Analytics uses adaptive sampling for older data. Keep the
reported sample interval and describe pageviews, visits and event counts as
estimates. Do not multiply a reported count by the sample interval. A zero in
a sampled subgroup does not prove that no visitor used it, and visits are not
unique people.

## Required monthly record

Write `analytics/traffic/YYYY-MM.json` and `analytics/traffic/YYYY-MM.md`.
Include:

- UTC period, collection timestamp, source dataset and sample interval.
- Estimated pageviews and visits, plus a daily series including zero days.
- Public route families and explicit locale path prefixes.
- Country, device class, browser family and operating system.
- Referrer hosts, with an empty host labelled `direct_or_unavailable`.
- P75 CLS, FCP, INP, LCP and TTFB, plus available good, needs-improvement and
  poor counts.
- The deployed build identifier and source commit when known.
- Plain-language findings, limitations and any correction note.

Normalize paths to known public routes and locale prefixes. Group unknown or
rare values as `other`. Country codes may remain at country level. Do not infer
a reader's language from country, browser language or IP geography. Explicit
locale paths are a lower bound because a reader can change language without a
new path being recorded.

## Privacy boundary

This repository is public. Store aggregate rows only, with a minimum published
cell size of twenty for country, referrer, browser and operating-system
buckets. Never store or derive:

- Raw request, beacon or event rows.
- IP addresses or precise locations.
- Visitor, device, session or advertising identifiers.
- Full user agents, versions or fingerprinting fields.
- Query strings, form values, free-text searches or URL fragments.
- Exact event timestamps.
- Referrer paths or full referrer URLs.
- Cross-dimension tables such as country by page or referrer by locale.

The collector should request only fields that can appear in the snapshot. Do
not download raw logs and then attempt to clean them afterward.

## Interpretation and corrections

The JSON file is canonical. The Markdown summary may round percentages but
must agree with the JSON counts. Snapshots are append-only. If source data was
wrong or a collection was incomplete, correct both files and add a dated note
that states the old value, new value and reason. Never silently rewrite older
months.

Do not compare a partial month with a completed month without labelling the
partial period. For interface priorities, combine traffic share with measured
task friction. High traffic does not by itself prove that a page works well,
and low traffic can be evidence that a page is hard to discover.

## Automation

The scheduled repository workflow runs on the second and third days of each
month. The second run is an idempotent retry. It uses a dedicated Cloudflare
token with only `Account Analytics:Read` and GitHub's built-in token with only
`contents: write`. It must never reuse or broaden the deployment token.

The repository secret is `CLOUDFLARE_ANALYTICS_TOKEN`. The non-secret account
ID and Web Analytics site tag are repository variables named
`CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_WEB_ANALYTICS_SITE_TAG`.
