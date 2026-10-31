"""画像を差し替えたあと、index.html の width / height 属性を実ファイルのサイズに合わせる。

- <img src="assets/img/..."> の width / height（CLS 防止用）
- OGP の og:image:width / og:image:height
実行: python3 lp/tools/sync_image_sizes.py        （書き換え）
      python3 lp/tools/sync_image_sizes.py --check（確認のみ。ずれがあれば終了コード 1）
"""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

IMG_TAG = re.compile(r'<img\b[^>]*\bsrc="(assets/img/[^"]+)"[^>]*>')
OGP_IMAGE = re.compile(r'<meta property="og:image" content="[^"]*/(assets/img/[^"]+)">')


def image_size(rel):
    with Image.open(ROOT / rel) as im:
        return im.size


def set_attr(tag, name, value):
    pattern = re.compile(r'\b%s="[^"]*"' % name)
    if pattern.search(tag):
        return pattern.sub('%s="%d"' % (name, value), tag)
    return tag.replace("<img", '<img %s="%d"' % (name, value), 1)


def main():
    check_only = "--check" in sys.argv
    html = HTML.read_text(encoding="utf-8")
    changes, missing = [], []

    def fix_img(m):
        tag, src = m.group(0), m.group(1)
        if not (ROOT / src).exists():
            missing.append(src)
            return tag
        w, h = image_size(src)
        new = set_attr(set_attr(tag, "width", w), "height", h)
        if new != tag:
            changes.append("%s -> %dx%d" % (src, w, h))
        return new

    html = IMG_TAG.sub(fix_img, html)

    ogp = OGP_IMAGE.search(html)
    if ogp and (ROOT / ogp.group(1)).exists():
        w, h = image_size(ogp.group(1))
        for name, value in (("og:image:width", w), ("og:image:height", h)):
            pattern = re.compile(r'(<meta property="%s" content=")\d+(">)' % name)
            new_html = pattern.sub(r"\g<1>%d\g<2>" % value, html)
            if new_html != html:
                changes.append("%s -> %d" % (name, value))
                html = new_html
        if (w, h) != (1200, 630):
            print("注意: OGP 画像は 1200x630 を推奨（現在 %dx%d）" % (w, h))
    elif ogp:
        missing.append(ogp.group(1))

    for src in sorted(set(missing)):
        print("見つからない画像: " + src)
    for c in changes:
        print(("要更新: " if check_only else "更新: ") + c)
    if not changes:
        print("width / height はすべて実画像と一致しています。")

    if check_only:
        sys.exit(1 if changes or missing else 0)
    if changes:
        HTML.write_text(html, encoding="utf-8")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
