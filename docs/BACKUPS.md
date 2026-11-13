# Plithos restore points

Backups are restore points, not working branches. Create one before a material
change to navigation, data structure, publishing, or site-wide behavior.

Each restore point has:

- An annotated Git tag on the validated integration-branch commit.
- GitHub's source ZIP generated from that tag.
- A source ZIP, full-history Git bundle, manifest and checksums stored outside
  GitHub in the owner's Google Drive.
- A clean-worktree check and the normal repository validations before tagging.

Do not place secrets, local settings, credentials, raw traffic logs or
untracked files in a backup.

## 13 November 2026 - before prayer redesign

- Tag: `backup-2026-11-13-pre-prayer-redesign`
- Branch at capture: `claude/plithos-org-code-247ox6`
- Live build identifier: `2026-10-07b`
- GitHub source ZIP:
  `https://github.com/plithosorthodox/plithos.org/archive/refs/tags/backup-2026-11-13-pre-prayer-redesign.zip`
- Independent Drive folder:
  `https://drive.google.com/drive/folders/1ag1DABpWD3kU-KowrPOy3Qqf07jxXP6a`

The Drive package is named
`plithos-complete-backup-2026-11-13-pre-prayer-redesign.zip`. Its manifest
records the exact tag, commit, archive sizes and SHA-256 checksums. A separate
`.sha256` file permits verification before the package is opened. The package
is stored in Drive as five ordered parts because the connected uploader has a
100 MB per-file limit. Download every part and follow `DRIVE-REASSEMBLE.txt`
before checking the package hash.

### Restore source only

Download and extract either source ZIP. Run:

```text
python tools/nav_chrome.py --check
python tools/check_site.py
```

The extracted source tree has no Git history.

### Restore the complete repository

Extract the Drive package, then clone the bundle:

```text
git clone plithos-history-backup-2026-11-13-pre-prayer-redesign.bundle plithos-restored
cd plithos-restored
git checkout backup-2026-11-13-pre-prayer-redesign
git bundle verify ../plithos-history-backup-2026-11-13-pre-prayer-redesign.bundle
```

Only reconnect a remote after the restored tree and tag have been inspected.
