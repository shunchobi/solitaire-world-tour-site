# SolitaireWorld 公開ページ

App Store / Google Play への申請に必要な **プライバシーポリシー** と **サポート** のページ。
素の HTML / CSS / JavaScript だけで作ってあり、ビルドも npm も使わない。

公開先: <https://shunchobi.github.io/solitaireworld-site/>

| ページ | URL | 用途 |
|---|---|---|
| `index.html` | `/` | アプリ紹介と 2 ページへの入口 |
| `privacy.html` | `/privacy.html` | **Apple / Google Play のプライバシーポリシー URL** |
| `support.html` | `/support.html` | **Apple のサポート URL** |

`?lang=ja` / `?lang=en` を付けると、その言語で開いた状態のリンクを渡せる。

> このフォルダは Unity プロジェクトのリポジトリの中にあるが、**別のリポジトリ**である。
> 親リポジトリ側では `.gitignore` で `/site/` を除外しているため、Unity 側のコミットには入らない。

## 中身

```
index.html / privacy.html / support.html   ページ本体(日英を両方持つ)
assets/style.css                           3 枚共通のスタイル
assets/lang.js                             言語トグルの配線
assets/favicon.svg
assets/fonts/*.woff2                       M PLUS Rounded 1c のサブセット
assets/fonts/OFL.txt                       フォントのライセンス(SIL OFL 1.1・同梱必須)
tools/build-fonts.py                       サブセットの生成
tools/check-fonts.py                       文字の欠落検査
```

## 文章を直したときにやること

**本文の文字を増やしたら、フォントのサブセットを作り直す。** サブセットにはページに出てくる
文字しか入っていないため、作り直さないと増やした文字だけ別のフォントで表示される。

```bash
python3 tools/build-fonts.py    # 作り直す
python3 tools/check-fonts.py    # 欠落が無いか検査する(欠けていたら失敗する)
```

サブセット元は Unity 側の `Assets/Resources/fonts/MPLUSRounded1c-{Regular,Bold}.ttf`。
このスクリプトは読むだけで、Unity 側のファイルには一切触れない。

かな・ラテン・約物は使っていない文字も丸ごと入れてあるので、少し文章を直した程度では
たいてい欠けない。欠けるとしたら新しい漢字を足したときで、それを `check-fonts.py` が捕まえる。

## 言語切り替えの仕組み

- 日英の本文は**どちらも HTML に書いてある**。CSS の既定では両方表示される
- `<head>` のインラインスクリプトが `<html>` に `class="js"` と `data-active-lang` を付け、
  CSS がその値を見て片方を隠す
- **JavaScript が無効な環境では両方がそのまま縦に並んで読める**(審査担当の環境を想定した作り)
- 表示言語の決定は `?lang=` → 前回の選択 → 端末の言語 の順

> `<head>` のインラインスクリプトは 3 ページに同じものが入っている。
> **直すときは 3 枚とも直すこと。** 描画前に走らせる必要があるため外部ファイルにできない。

## 配色の制約

`docs/design/worldview.md` のカラートークンを使っているが、**そのままでは文字に使えない色がある**。
クリーム地 `#FBF7EE` 上での実測コントラスト比:

| 色 | 比 | 文字に使えるか |
|---|---|---|
| `#5A4636` ink | 8.30:1 | ○ 本文 |
| `#6E5A44` pinStroke | 6.12:1 | ○ 副次テキスト |
| `#C4442D` | 4.66:1 | ○ リンク文字 |
| `#8C7458` inkSoft | 4.13:1 | × 通常サイズには不足 |
| `#E85C43` vermilion | 3.25:1 | × 装飾のみ |
| `#B0A085` inkMuted | 2.39:1 | × 装飾のみ |

純黒 `#000000` は使わない(`docs/design/art-bible.md` の禁則)。影は暖かいセピアで作る。

## ローカルでの確認

**サイトフォルダの 1 つ上から**配信する。公開先が `/solitaireworld-site/` 配下になるため、
同じ入れ子で見ておくとリンクの書き方の誤りに気付ける。

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory ..
# → http://127.0.0.1:4173/site/
```

## 公開

GitHub Pages の設定は Settings → Pages → Source: **Deploy from a branch** /
Branch: `main` / フォルダ: `/ (root)`。`.nojekyll` を置いてあるので Jekyll のビルドは走らない。

```bash
git add -A && git commit -m "..." && git push
```

反映まで 1〜3 分かかる。Actions タブの `pages build and deployment` の成功が本当の合図。
