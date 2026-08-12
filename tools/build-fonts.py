#!/usr/bin/env python3
"""M PLUS Rounded 1c の woff2 サブセットを作り直す。

このサイトはページに出てくる文字だけを含めたサブセットを自己ホストしている
(Google Fonts の CDN を読むと、閲覧者の IP がプライバシーポリシーのページから
Google に渡ってしまうため)。

そのため **HTML の本文を書き換えたら必ずこれを実行する**。
実行しないと、増やした文字だけが別のフォントで表示される。
検査は tools/check-fonts.py で行う。

使い方:
    python3 site/tools/build-fonts.py

必要なもの: fontTools(pyftsubset)と brotli。どちらも導入済み。
"""

from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
REPO = SITE.parent
PAGES = ["index.html", "privacy.html", "support.html"]

# サブセット元。Unity 側の実機アセットをそのまま使う(コピーも改変もしない)。
SOURCES = {
    "400": REPO / "Assets/Resources/fonts/MPLUSRounded1c-Regular.ttf",
    "700": REPO / "Assets/Resources/fonts/MPLUSRounded1c-Bold.ttf",
}

# ページに今出ていなくても常に入れておく範囲。
# かな・ラテン・約物は全体から見て安価な一方、あとで文章を直したときに
# 最も欠けやすいので、保険として丸ごと含めておく。
ALWAYS = ",".join([
    "U+0020-007E",   # 基本ラテン
    "U+00A0-00FF",   # ラテン1補助
    "U+2010-2027",   # ダッシュ・引用符
    "U+2030-205E",   # 一般約物
    "U+2190-2193",   # 矢印
    "U+25A0-25FF",   # 幾何学記号(◆ など)
    "U+2660-2667",   # トランプのスート
    "U+3000-303F",   # CJK の約物
    "U+3040-309F",   # ひらがな
    "U+30A0-30FF",   # カタカナ
    "U+FF01-FF60",   # 全角形
    "U+FFE0-FFE6",   # 全角記号
])


def page_characters() -> set[str]:
    """3 ページに現れる文字をすべて集める。

    実体参照(&rsquo; など)は展開してから数える。展開しないと、
    実体参照でしか書かれていない文字がサブセットから漏れる。
    """
    chars: set[str] = set()
    for name in PAGES:
        source = (SITE / name).read_text(encoding="utf-8")
        chars.update(html.unescape(source))
    return chars


def build(weight: str, text: str) -> Path:
    src = SOURCES[weight]
    if not src.exists():
        sys.exit(f"サブセット元が見つからない: {src}")

    out = SITE / "assets/fonts" / f"mplus-rounded1c-{weight}.woff2"
    text_file = SITE / "tools" / f".chars-{weight}.txt"
    text_file.write_text(text, encoding="utf-8")

    try:
        subprocess.run(
            [
                sys.executable, "-m", "fontTools.subset", str(src),
                f"--text-file={text_file}",
                f"--unicodes={ALWAYS}",
                "--layout-features=kern",
                "--flavor=woff2",
                f"--output-file={out}",
            ],
            check=True,
        )
    finally:
        text_file.unlink(missing_ok=True)

    return out


def main() -> None:
    chars = page_characters()
    text = "".join(sorted(chars))
    print(f"ページに出てくる異なり文字数: {len(chars)}")

    total = 0
    for weight in ("400", "700"):
        out = build(weight, text)
        size = out.stat().st_size
        total += size
        print(f"  {out.name}: {size / 1024:.1f} KB")

    print(f"合計: {total / 1024:.1f} KB")
    print("\n続けて python3 site/tools/check-fonts.py で欠落が無いか確認すること。")


if __name__ == "__main__":
    main()
