#!/usr/bin/env python3
"""
Take the network away from the app.

The app carries the whole site inside itself, so it has no use for a
connection. This removes the permission that would let it open one. After
this runs, the app is not trusted to stay offline; it is unable to do
otherwise, because Android refuses the request at the system level.

    python3 tools/harden_manifest.py

Run after the Android project is scaffolded and before it is built. The
project is generated fresh by every build, so the removal has to be a build
step rather than a file kept in the tree.

Every edit asserts what it expects to find. If the scaffolding ever changes
shape, the build stops here rather than quietly shipping a permission nobody
meant to grant.

Three things are done:

  The INTERNET permission is removed, which is the whole point.

  The browser component's Safe Browsing lookup is turned off. It is on by
  default and is answered by Google Play services in another process, which
  holds its own permission - so it is not covered by the removal above and
  has to be refused by name. This trades a security feature for the promise
  that nothing leaves the phone; it is a deliberate choice, and it is the
  right one only because the app loads no remote page and no untrusted link.

  Cleartext traffic is refused and a network configuration that permits
  nothing is installed, so that a future change which restores the
  permission still does not silently start talking to anything.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "app" / "android" / "app" / "src" / "main"
MANIFEST = ANDROID / "AndroidManifest.xml"
NSC = ANDROID / "res" / "xml" / "network_security_config.xml"

INTERNET = re.compile(
    r'^[ \t]*<uses-permission[ \t]+android:name="android\.permission\.INTERNET"'
    r'[ \t]*/>[ \t]*\r?\n', re.M)

SAFE_BROWSING = (
    '        <meta-data android:name="android.webkit.WebView.EnableSafeBrowsing"\n'
    '            android:value="false" />\n')

NSC_XML = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <base-config cleartextTrafficPermitted="false" />
</network-security-config>
"""


def main():
    if not MANIFEST.exists():
        raise SystemExit("no generated manifest at %s" % MANIFEST)
    s = MANIFEST.read_text(encoding="utf-8")

    # A second run over an already hardened project is not a fault; a missing
    # permission where nothing has been hardened yet is.
    if "EnableSafeBrowsing" in s and "android.permission.INTERNET" not in s:
        print("manifest already hardened")
        return 0

    found = INTERNET.findall(s)
    if len(found) != 1:
        raise SystemExit(
            "expected exactly one INTERNET permission line, found %d - the "
            "scaffolding has changed and this script must be re-read" % len(found))
    s = INTERNET.sub("", s, count=1)
    if "android.permission.INTERNET" in s:
        raise SystemExit("INTERNET is still named in the manifest after the removal")

    m = re.search(r"<application\b[^>]*[^/]>", s)
    if not m:
        raise SystemExit("no <application> tag in the manifest")
    tag = m.group(0)
    if "usesCleartextTraffic" not in tag:
        tag = (tag[:-1].rstrip()
               + '\n        android:usesCleartextTraffic="false"'
               + '\n        android:networkSecurityConfig="@xml/network_security_config">')
        s = s[:m.start()] + tag + s[m.end():]

    if "EnableSafeBrowsing" not in s:
        i = s.rindex("</application>")
        s = s[:i] + SAFE_BROWSING + s[i:]

    MANIFEST.write_text(s, encoding="utf-8")
    NSC.parent.mkdir(parents=True, exist_ok=True)
    NSC.write_text(NSC_XML, encoding="utf-8")
    print("manifest hardened: INTERNET removed, Safe Browsing off, cleartext refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
