#!/usr/bin/env python3
"""
Give the app the mark the site wears.

The Plithos P - the letter drawn as a staff with a crossbar, in the site's
ground colour - is the same figure the pages carry as their favicon. This
writes it into the generated Android project as a launcher icon.

    python3 tools/app_icon.py

Run after the Android project is scaffolded. Nothing is installed to draw it:
the mark is three strokes and a circle, so it is drawn here directly and
written out as PNG, and given to newer systems as a scalable drawing they can
mask into whatever shape the reader's launcher uses.
"""
import math
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "app" / "android" / "app" / "src" / "main" / "res"

GROUND = (0x6e, 0x2b, 0x3b)     # porphyry, the site's own red
MARK = (0xf2, 0xec, 0xe0)       # the warm off-white the pages write in

# The figure, in the hundred-unit square the favicon is drawn in.
STEM = ((45, 20), (45, 82))
BAR = ((30, 51), (60, 51))
BOWL = ((45, 20), (61, 20), (67, 26), (67, 33))     # cubic, upper half
BOWL2 = ((67, 33), (67, 40), (61, 46), (45, 46))    # cubic, lower half
STROKE = 7.0

# Android's five densities, and the pixel size of a launcher icon at each.
DENSITIES = [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96),
             ("xxhdpi", 144), ("xxxhdpi", 192)]


def bezier(p, n=48):
    """A cubic sampled into a polyline; the mark has no curve fine enough to
    need more than this."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u*u*u*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t*x3,
                    u*u*u*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t*y3))
    return out


def segments():
    """Each segment with the box it can possibly darken, so a pixel far from
    a stroke costs a comparison rather than a square root."""
    segs = [STEM, BAR]
    for curve in (BOWL, BOWL2):
        pts = bezier(curve)
        segs += list(zip(pts, pts[1:]))
    half = STROKE / 2.0
    out = []
    for a, b in segs:
        out.append((a, b,
                    min(a[0], b[0]) - half, max(a[0], b[0]) + half,
                    min(a[1], b[1]) - half, max(a[1], b[1]) + half))
    return out


def dist_to_seg(px, py, a, b):
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)))
    return math.hypot(px - (ax + t*dx), py - (ay + t*dy))


def render(size, disc=True, inset=1.0, samples=3):
    """The mark at a given pixel size. With disc, the porphyry circle behind
    it; without, the strokes alone on nothing, which is what a newer system
    wants so it can lay them on a background of its own."""
    segs = segments()
    half = STROKE / 2.0
    px = bytearray()
    step = 1.0 / (samples + 1)
    scale = 100.0 / size / inset
    off = (100.0 / inset - 100.0) / 2.0
    for y in range(size):
        row = bytearray()
        for x in range(size):
            r = g = b = a = 0.0
            hits = 0
            for sy in range(samples):
                for sx in range(samples):
                    ux = (x + (sx + 1) * step) * scale - off
                    uy = (y + (sy + 1) * step) * scale - off
                    hits += 1
                    on_mark = False
                    for p0, p1, x0, x1, y0, y1 in segs:
                        if x0 <= ux <= x1 and y0 <= uy <= y1 \
                                and dist_to_seg(ux, uy, p0, p1) <= half:
                            on_mark = True
                            break
                    inside = (ux - 50) ** 2 + (uy - 50) ** 2 <= 47 * 47
                    if on_mark and (inside or not disc):
                        r += MARK[0]; g += MARK[1]; b += MARK[2]; a += 255
                    elif disc and inside:
                        r += GROUND[0]; g += GROUND[1]; b += GROUND[2]; a += 255
            row += bytes((int(r / hits), int(g / hits), int(b / hits), int(a / hits)))
        px += b"\x00" + row
    return png(size, size, bytes(px))


def png(w, h, raw):
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def path_data():
    def c(p):
        return "M%g,%g C%g,%g %g,%g %g,%g" % (p[0][0], p[0][1], p[1][0], p[1][1],
                                              p[2][0], p[2][1], p[3][0], p[3][1])
    return ["M%g,%g L%g,%g" % (STEM[0][0], STEM[0][1], STEM[1][0], STEM[1][1]),
            "M%g,%g L%g,%g" % (BAR[0][0], BAR[0][1], BAR[1][0], BAR[1][1]),
            c(BOWL), c(BOWL2)]


def vector_foreground():
    paths = "\n".join(
        '    <path android:pathData="%s"\n'
        '        android:strokeColor="#f2ece0" android:strokeWidth="%g"\n'
        '        android:strokeLineCap="butt" android:strokeLineJoin="miter" />'
        % (d, STROKE) for d in path_data())
    # The mark is laid inside the safe area a launcher may crop to.
    return ('<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            '    android:width="108dp" android:height="108dp"\n'
            '    android:viewportWidth="108" android:viewportHeight="108">\n'
            '  <group android:scaleX="0.66" android:scaleY="0.66"\n'
            '      android:translateX="21" android:translateY="21">\n'
            + paths + "\n  </group>\n</vector>\n")


VECTOR_BACKGROUND = (
    '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
    '    android:width="108dp" android:height="108dp"\n'
    '    android:viewportWidth="108" android:viewportHeight="108">\n'
    '  <path android:pathData="M0,0 h108 v108 h-108 z" android:fillColor="#6e2b3b" />\n'
    '</vector>\n')

ADAPTIVE = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
    '    <background android:drawable="@drawable/ic_launcher_background" />\n'
    '    <foreground android:drawable="@drawable/ic_launcher_foreground" />\n'
    '</adaptive-icon>\n')


def main():
    if not RES.exists():
        raise SystemExit("no generated res/ at %s - scaffold the project first" % RES)

    (RES / "drawable").mkdir(parents=True, exist_ok=True)
    (RES / "drawable" / "ic_launcher_foreground.xml").write_text(
        vector_foreground(), encoding="utf-8")
    (RES / "drawable" / "ic_launcher_background.xml").write_text(
        VECTOR_BACKGROUND, encoding="utf-8")

    (RES / "mipmap-anydpi-v26").mkdir(parents=True, exist_ok=True)
    for n in ("ic_launcher.xml", "ic_launcher_round.xml"):
        (RES / "mipmap-anydpi-v26" / n).write_text(ADAPTIVE, encoding="utf-8")

    for name, size in DENSITIES:
        d = RES / ("mipmap-" + name)
        d.mkdir(parents=True, exist_ok=True)
        blob = render(size)
        for n in ("ic_launcher.png", "ic_launcher_round.png"):
            (d / n).write_bytes(blob)
        # The separate foreground some templates ask for, strokes alone.
        (d / "ic_launcher_foreground.png").write_bytes(
            render(size, disc=False, inset=0.66))
    print("icon written: %d densities, and a scalable drawing for newer systems"
          % len(DENSITIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
