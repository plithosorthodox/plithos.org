# Deploying plithos.org

Written for someone who has not used GitHub before. Read the first section
before doing anything - you may not need the GitHub Action at all.

---

## First: you probably want Option A

There are two ways to get this repository onto Cloudflare Pages, and the
snippet you found is the more complicated of the two.

### Option A - Cloudflare watches GitHub (recommended)

Cloudflare connects itself to the repository and deploys on every push. No
API token, no secrets, no workflow file, nothing to maintain.

**This is the right choice here** because the site has no build step. The
files in the repository are exactly what is served, so there is nothing for a
CI runner to do that Cloudflare cannot do itself.

Setup, once:

1. Cloudflare dashboard -> **Workers & Pages** -> your Pages project
2. **Settings** -> **Builds & deployments** -> **Connect to Git**
3. Pick `plithosorthodox/plithos.org`
4. Production branch: **`main`**
5. Framework preset: **None**. Build command: **leave empty**.
   Build output directory: **`/`**
6. Save

Done. Every push to `main` deploys in about 30 seconds, and every pull
request gets its own preview URL automatically.

> **Note:** you said you connected your GitHub *account* to Cloudflare. That
> is only the authorisation step. You still have to connect this specific
> *repository* to this specific Pages *project*, which is step 3 above.

### Option B - GitHub Actions pushes to Cloudflare

Use this only if you later need something to happen before deploying that
Cloudflare cannot do - for example running `tools/build_search_index.py`
automatically, or blocking a bad deploy on `tools/check_site.py`.

`.github/workflows/deploy.yml` in this repository already does Option B.
**It sits dormant until you add the credentials below.** Without them the
workflow fails, harmlessly, and nothing deploys.

**One correction to the snippet you sent:** `cloudflare/pages-action@1` is
[deprecated](https://github.com/cloudflare/pages-action). The current action
is [`cloudflare/wrangler-action`](https://github.com/cloudflare/wrangler-action),
which is what the workflow uses.

Setup:

1. **Create an API token.** Cloudflare dashboard -> your user icon ->
   **My Profile** -> **API Tokens** -> **Create Token** -> **Custom Token**.
   Permission: **Account -> Cloudflare Pages -> Edit**. Create, and copy the
   token - it is shown once.

2. **Find your account ID.** It is in the dashboard URL:
   `https://dash.cloudflare.com/<ACCOUNT_ID>/pages`

3. **Add them to GitHub.** Repository -> **Settings** -> **Secrets and
   variables** -> **Actions**:

   | Where | Name | Value |
   |---|---|---|
   | Secrets tab | `CLOUDFLARE_API_TOKEN` | the token from step 1 |
   | Secrets tab | `CLOUDFLARE_ACCOUNT_ID` | the ID from step 2 |
   | Variables tab | `CLOUDFLARE_PROJECT_NAME` | your Pages project name |

The account ID is not really a secret, but keeping it out of the file means
the workflow can be public without listing your account.

**Do not use both options at once** - you would get two deploys per push.

---

## How you approve changes

This matters for your rule about keeping executive approval over content.

**The pull request is the approval gate.** Nothing I push can reach
plithos.org on its own, because I only ever push to a branch, and only `main`
deploys.

```
  I push a branch  ->  you open a pull request  ->  you read the diff
                                                          |
                          you merge  <-  you approve  <----+
                              |
                       main deploys automatically
```

To review a change:

1. Go to the repository on GitHub. A yellow banner offers **Compare & pull
   request** for the branch I pushed. Click it, then **Create pull request**.
2. The **Files changed** tab shows every line, red for removed and green for
   added.
3. If Option A is set up, Cloudflare posts a **preview URL** on the pull
   request - the whole site, built from that branch, on a real address. Click
   it and use it before deciding.
4. Happy: **Merge pull request**. Not happy: leave a comment, or **Close**
   it, and nothing changes.

For content specifically: any added prayer, saint's life, or patristic text
arrives as a pull request with its provenance in the description. Read it,
verify it, then merge. Nothing goes live unread.

---

## Rolling back

Two ways, both fast:

- **Cloudflare:** dashboard -> your Pages project -> **Deployments** ->
  find the last good one -> **Rollback to this deployment**. Immediate.
- **Git:** on the merged pull request, click **Revert**. That opens a new
  pull request undoing the change; merge it and the site redeploys.

---

## The cache trap

`_headers` caches `/data/prayers-i18n.v1.*`, `/data/bible.v1.*` and
`/data/search-index.v1.json` as **immutable for one year**. That is what the
`v1` in the filename is for.

If you change one of those files **you must bump the version in its
filename** - `v1` to `v2` - and update every reference in the HTML.
Otherwise returning visitors keep the old copy for up to a year and you will
think the deploy failed.

Files without a version in the name are not cached that way:
`/data/library/*` is one hour, `/scripture/*` and `/assets/*` are one week.
Note the week on `/assets/*`: a change to the shared UI takes up to seven
days to reach returning visitors.

---

## Checking before you deploy

```bash
python3 tools/check_site.py
```

Catches the failures that are invisible in a browser - a catalogue entry with
no file, a fetch target that does not exist, a stale search index, a page
that lost the shared UI layer. Cloudflare Pages answers a missing path with
HTTP 200 and the whole 6.8 MB of `index.html`, so a broken link to a data
file looks perfectly fine until you measure it. Three separate bugs on this
site came from exactly that.

Under Option B this runs automatically and a failure blocks the deploy.

To preview locally:

```bash
python3 -m http.server 8000    # http://localhost:8000
```

`_headers` and `_redirects` are Cloudflare directives and do nothing locally,
so extensionless routes like `/saints` only work in production.
