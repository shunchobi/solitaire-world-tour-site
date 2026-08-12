#!/usr/bin/env python3
"""woff2 サブセットに文字の欠落が無いか検査する。

テキスト駆動のサブセットは、本文に文字を足したあと再生成を忘れると
その 1 文字だけ別のフォントで表示される。見た目の差が小さく気付きにくいので、
規律ではなく検査で潰す。欠落があれば終了コード 1 で落とす。

使い方:
    python3 site/tools/check-fonts.py
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

SITE = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "privacy.html", "support.html"]
FONTS = ["mplus-rounded1c-400.woff2", "mplus-rounded1c-700.woff2"]

# フォントが持っている必要のない文字。改行・タブや、字形を持たない制御文字。
IGNORED = set("\n\r\t﻿")


def needed_characters() -> set[str]:
    chars: set[str] = set()
    for name in PAGES:
        chars.update(html.unescape((SITE / name).read_text(encoding="utf-8")))
    return {c for c in chars if c not in IGNORED}


def covered(font_path: Path) -> set[int]:
    with TTFont(font_path, lazy=True) as font:
        return set(font.getBestCmap().keys())


def main() -> int:
    needed = needed_characters()
    failed = False

    for name in FONTS:
        path = SITE / "assets/fonts" / name
        if not path.exists():
            print(f"NG {name}: ファイルが無い。先に build-fonts.py を実行すること")
            failed = True
            continue

        have = covered(path)
        missing = sorted(c for c in needed if ord(c) not in have)

        if missing:
            failed = True
            shown = "".join(missing[:60])
            print(f"NG {name}: {len(missing)} 文字が欠けている → {shown}")
        else:
            print(f"OK {name}: {len(needed)} 文字すべてを含む ({path.stat().st_size / 1024:.1f} KB)")

    if failed:
        print("\nsite/tools/build-fonts.py を実行してサブセットを作り直すこと。")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
