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
| `tools/generate_placeholder_images.py` | 仮画像の生成スクリプト |

## 仕様との対応

| 仕様 | 実装 |
| --- | --- |
| S02 / C01 OS 判定（7 章） | `<head>` のインラインスクリプトで `html[data-os]` を設定し、CSS で出し分け。iOS / Android は 1 つ、判定不可（PC 等）は両方表示 |
| C01 追従バー（5 章） | S02 を `IntersectionObserver` で監視。A: S02 が画面内 → 非表示 / B: S02 が上に抜けたら表示 / C: フッター到達時も表示を続け、フッターにバー分 + `env(safe-area-inset-bottom)` の余白 |
| スライダー（6 章） | `scroll-snap` によるネイティブスワイプ + 左右矢印 + ドット。矢印は端でループ |
| 画像見出し（7 章） | `h2` の中に `img` を置き、`alt` を設定 |
| 画像（7 章） | WebP。KV 以外は `loading="lazy"`。全画像で `width` / `height` を指定（CLS 対策） |
| 外部リンク（7 章） | `config.js` の URL を反映し、`target="_blank" rel="noopener noreferrer"` を付与 |

## 本番化の前に差し替えるもの

- `assets/img/` の画像一式（同じファイル名・同じ縦横比で置き換えれば、HTML の変更は不要）
- ストアバッジ：**Apple / Google の公式バッジ**に差し替えること（現在は仮画像）
- `assets/js/config.js` の URL と、`index.html` の OGP URL（`og:url` / `og:image` / `twitter:site`）
- テキスト（報酬名・注釈・キャラ名・説明・権利表記）
- 本文フォントは仮で Zen Maru Gothic（Google Fonts）を使っています（書体名は要確認：10 章 No.5）
