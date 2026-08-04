#!/usr/bin/env python3
"""
Repair five characters lost from the Chinese New Testament.

The Union Version bundle carried five replacement characters, in Matthew
6:19, Matthew 6:20, Colossians 1:29 and twice in James 5:3. They came in
with the text rather than from anything done here, and the same damage is
present in other copies of this edition circulating online, so it was
inherited rather than introduced.

Every replacement is sourced and none is inferred from context:

  Matthew 6:19, 6:20, James 5:3 (twice)   銹, from the Union Version text at
  Chinese Wikisource: 蟲子咬、能銹壞 and 金銀都長了銹．那銹要證明.

  Colossians 1:29                          裡, in "照著他在我裡面運用的大能".
  Wikisource prints 裏 here, the older form. This edition uses 裡 one thousand
  two hundred and eighty times and 裏 not once, so it takes 裡: the character
  is chosen to match the edition being published, not a different printing.

The bundle version is bumped because /data is served immutable for a year.
A repaired file under the old name would never reach anyone who already has
the broken one.

    python3 tools/fix_zh_nt.py --check
    python3 tools/fix_zh_nt.py --write
"""
import argparse
import base64
import json
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "bible.v1.zh.b64"
OUT = ROOT / "data" / "bible.v2.zh.b64"

# book, chapter, verse -> the reading this edition should carry. The whole
# verse is given rather than a character, so a patch that lands on the wrong
# verse fails instead of quietly editing Scripture.
REPAIRS = {
    ("Matthew", "6", "19"):
        "不 要 為 自 己 積 儹 財 寶 在 地 上 ； 地 上 有 蟲 子 咬 ， 能 銹 壞 ， "
        "也 有 賊 挖 窟 窿 來 偷 。",
    ("Matthew", "6", "20"):
        "只 要 積 儹 財 寶 在 天 上 ； 天 上 沒 有 蟲 子 咬 ， 不 能 銹 壞 ， "
        "也 沒 有 賊 挖 窟 窿 來 偷 。",
    ("Colossians", "1", "29"):
        "我 也 為 此 勞 苦 ， 照 著 他 在 我 裡 面 運 用 的 大 能 盡 心 竭 力 。",
    ("James", "5", "3"):
        "你 們 的 金 銀 都 長 了 銹 ； 那 銹 要 證 明 你 們 的 不 是 ， 又 要 吃 "
        "你 們 的 肉 ， 如 同 火 燒 。 你 們 在 這 末 世 只 知 積 儹 錢 財 。",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    d = json.loads(zlib.decompress(base64.b64decode(SRC.read_bytes())))
    zh = d["zh"]

    for (book, chap, verse), want in REPAIRS.items():
        have = zh.get(book, {}).get(chap, {}).get(verse)
        if have is None:
            print("%s %s:%s is not in the bundle" % (book, chap, verse))
            return 1
        if "�" not in have:
            print("%s %s:%s carries no replacement character; "
                  "it may already be repaired" % (book, chap, verse))
            return 1
        # The repair must differ from what is there only where the damage is.
        if have.replace("�", "") != want.replace("銹", "").replace("裡", ""):
            shown = have.replace("�", "[?]")
            print("%s %s:%s does not match the reading being written.\n"
                  "  in the bundle: %s\n  being written: %s"
                  % (book, chap, verse, shown, want))
            return 1
        zh[book][chap][verse] = want
        print("  %-14s %s:%-3s repaired" % (book, chap, verse))

    left = sum(t.count("�") for b, chs in zh.items() if b != "__metadata__"
               for c, vs in chs.items() for t in vs.values())
    print("\nreplacement characters remaining: %d" % left)
    if left:
        return 1

    if args.write:
        blob = zlib.compress(json.dumps(d, ensure_ascii=False,
                                        separators=(",", ":")).encode("utf-8"), 9)
        OUT.write_bytes(base64.b64encode(blob))
        print("wrote %s (%s bytes)"
              % (OUT.relative_to(ROOT), format(OUT.stat().st_size, ",")))
    elif not args.check:
        print("nothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
