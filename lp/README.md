# 事前登録 LP サンプル

「事前登録 LP サイト制作仕様書 v0.7」に沿った静的 LP のサンプル実装です。
画像・テキスト・キャラクターはすべてオリジナルの**仮素材**で、ベンチマークの素材は使っていません。

## 確認方法

```sh
cd lp
python3 -m http.server 8000
# → http://localhost:8000/
```

## 構成

| パス | 内容 |
| --- | --- |
| `index.html` | ページ本体（S01〜S07、C01）。OGP / Twitter カードも `<head>` に記載 |
| `assets/css/style.css` | スタイル（SP 優先、480px で幅固定・中央寄せ、ブレークポイントなし） |
| `assets/js/config.js` | **URL 設定（ストア / SNS / 規約・PP・問い合わせ）を一元管理** |
| `assets/js/main.js` | 外部リンク反映、C01 追従バー、スライダー（S04 / S05） |
| `assets/img/` | 仮画像（WebP。OGP のみ互換性のため PNG） |
| `tools/generate_placeholder_images.py` | 仮画像の生成スクリプト（**本番画像を上書きするので、差し替え後は実行しないこと**） |
| `tools/sync_image_sizes.py` | 画像差し替え後に HTML の width / height を実画像に合わせるスクリプト |

## 仕様との対応

| 仕様 | 実装 |
| --- | --- |
| S02 / C01 OS 判定（7 章） | `<head>` のインラインスクリプトで `html[data-os]` を設定し、CSS で出し分け。iOS / Android は 1 つ、判定不可（PC 等）は両方表示 |
| C01 追従バー（5 章） | ご指示により**初期表示から常時表示**（仕様書の状態A「初期は非表示」から変更）。フッターにバー分 + `env(safe-area-inset-bottom)` の余白 |
| スライダー（6 章） | `scroll-snap` によるネイティブスワイプ + 左右矢印 + ドット。矢印は端でループ |
| 画像見出し（7 章） | `h2` の中に `img` を置き、`alt` を設定 |
| 画像（7 章） | WebP。KV 以外は `loading="lazy"`。全画像で `width` / `height` を指定（CLS 対策） |
| 外部リンク（7 章） | `config.js` の URL を反映し、`target="_blank" rel="noopener noreferrer"` を付与 |

## 仮素材の差し替え手順

### 画像

1. `assets/img/` の同名ファイルを本番画像で上書きする（解像度・縦横比は自由）
2. 次を実行して、HTML の `width` / `height` 属性（CLS 防止用）と OGP のサイズを実画像に合わせる

   ```sh
   python3 lp/tools/sync_image_sizes.py          # 書き換え
   python3 lp/tools/sync_image_sizes.py --check  # 確認のみ（ずれがあれば終了コード 1）
   ```

表示サイズは CSS で幅（% 指定）を決め、高さは画像の縦横比に従います。そのため、画像のピクセル数が変わっても見た目の幅は変わりません。
推奨サイズは、表示幅（最大 480px）の 2 倍程度です。

| ファイル | 用途 | 表示幅（480px 時） | 仮素材のサイズ | 備考 |
| --- | --- | --- | --- | --- |
| `kv.webp` | S01 メイン画像 | 480px | 750×900 | 上部にロゴが重なる（`.kv__logo` の `top` で位置調整） |
| `logo.webp` | S01 ロゴ | 約 375px | 600×220 | 透過推奨 |
| `badge_appstore.webp` / `badge_googleplay.webp` | S02 / C01 ストアボタン | 140〜220px | 360×108 | **公式バッジに差し替え必須**。縦横比が違ってもよい |
| `h_reward` / `h_game` / `h_chara` / `h_sns` `.webp` | 見出し画像 | 約 420px | 640×110 | 透過推奨。文言は HTML の `alt` も合わせて変更 |
| `reward_1〜3.webp` | S03 報酬画像 | 約 250px | 400×300 | |
| `ss_1〜3.webp` | S04 スクショ | 約 360px | 540×960 | 3 枚の縦横比をそろえると、スライダーの高さがそろう |
| `chara_1〜4.webp` | S05 キャラ画像 | 約 220px | 400×400 | 正方形推奨。正方形でなくても中央を円形に切り抜いて表示 |
| `arrow_left` / `arrow_right` `.webp` | スライダー矢印 | 40px | 96×96 | |
| `ogp.png` | OGP / Twitter カード | — | 1200×630 | 1200×630 推奨 |

ファイル名や拡張子を変える場合（例：公式バッジを SVG で使う）は、`index.html` の `src` も書き換えてから、上のスクリプトを実行してください。

### テキスト・URL・その他

- テキスト：仮の文言はすべて `index.html` 内に「（仮）」付きで書いてあります（`grep -n "（仮）" lp/index.html` で一覧できます）。報酬名・注釈・キャラ名・説明・権利表記・`<title>` / OGP の文言が対象です
- URL：`assets/js/config.js`（ストア / SNS / 規約・PP・問い合わせ）と、`index.html` の OGP URL（`og:url` / `og:image` / `twitter:site`）
- フォント：本文は仮で Zen Maru Gothic（Google Fonts）を使っています（書体名は要確認：10 章 No.5）。変更は `style.css` の `--font-body` と `index.html` のフォント読み込みで行います
- 色：`style.css` 冒頭の `:root` の変数でまとめて変えられます
