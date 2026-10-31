"""LP サンプル用の仮画像（オリジナル）を生成する。

本番素材が揃ったら assets/img/ の同名ファイルを差し替えればよい。
実行: python3 lp/tools/generate_placeholder_images.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"
SS = 2  # スーパーサンプリング倍率

CREAM = (255, 246, 220)
CREAM_DARK = (250, 230, 180)
BROWN = (122, 82, 48)
TEAL = (62, 155, 168)
ORANGE = (242, 169, 59)
PINK = (244, 160, 170)
GREEN = (126, 196, 120)
BLUE = (110, 160, 230)
PURPLE = (176, 140, 220)
WHITE = (255, 255, 255)
BLOCK_COLORS = [ORANGE, PINK, GREEN, BLUE, PURPLE, TEAL]


def font(size):
    return ImageFont.truetype(FONT_PATH, size * SS)


def canvas(w, h, bg):
    img = Image.new("RGBA", (w * SS, h * SS), bg)
    return img, ImageDraw.Draw(img)


def s(*v):
    return tuple(x * SS for x in v)


def save(img, name, w, h, fmt="WEBP"):
    img = img.resize((w, h), Image.LANCZOS)
    path = OUT / name
    if fmt == "WEBP":
        img.save(path, "WEBP", quality=88, method=6)
    else:
        img.convert("RGB").save(path, fmt)
    print("wrote", path.relative_to(OUT.parent.parent))


def center_text(d, cx, cy, text, size, fill, stroke=0, stroke_fill=None):
    d.text((cx * SS, cy * SS), text, font=font(size), fill=fill, anchor="mm",
           stroke_width=stroke * SS, stroke_fill=stroke_fill)


def draw_critter(d, cx, cy, r, color, ear="round"):
    """オリジナルの仮キャラ（丸い動物）を描く。"""
    if ear == "round":
        for dx in (-0.65, 0.65):
            d.ellipse(s(cx + dx * r - r * 0.32, cy - r * 0.95, cx + dx * r + r * 0.32, cy - r * 0.31), fill=color)
    elif ear == "cat":
        for sign in (-1, 1):
            d.polygon([s(cx + sign * r * 0.85, cy - r * 0.3), s(cx + sign * r * 0.75, cy - r * 1.05),
                       s(cx + sign * r * 0.2, cy - r * 0.8)], fill=color)
    elif ear == "long":
        for dx in (-0.35, 0.35):
            d.ellipse(s(cx + dx * r - r * 0.2, cy - r * 1.6, cx + dx * r + r * 0.2, cy - r * 0.5), fill=color)
    d.ellipse(s(cx - r, cy - r * 0.85, cx + r, cy + r * 0.95), fill=color)
    d.ellipse(s(cx - r * 0.45, cy + r * 0.05, cx + r * 0.45, cy + r * 0.6), fill=WHITE)
    for dx in (-0.38, 0.38):
        d.ellipse(s(cx + dx * r - r * 0.09, cy - r * 0.2, cx + dx * r + r * 0.09, cy - r * 0.02), fill=BROWN)
    d.ellipse(s(cx - r * 0.1, cy + r * 0.12, cx + r * 0.1, cy + r * 0.26), fill=BROWN)
    for dx in (-0.62, 0.62):
        d.ellipse(s(cx + dx * r - r * 0.13, cy + r * 0.1, cx + dx * r + r * 0.13, cy + r * 0.24), fill=PINK)


def block_grid(d, x0, y0, cols, rows, size, gap, seed=0):
    for row in range(rows):
        for col in range(cols):
            c = BLOCK_COLORS[(row * 7 + col * 3 + seed) % len(BLOCK_COLORS)]
            x = x0 + col * (size + gap)
            y = y0 + row * (size + gap)
            d.rounded_rectangle(s(x, y, x + size, y + size), radius=size * 0.25 * SS, fill=c)
            d.ellipse(s(x + size * 0.18, y + size * 0.15, x + size * 0.42, y + size * 0.35), fill=(255, 255, 255, 140))


def kv():
    w, h = 750, 900
    img, d = canvas(w, h, CREAM)
    for i, c in enumerate(BLOCK_COLORS * 3):
        x = (i * 137) % w
        y = (i * 211) % 260 + 260
        d.rounded_rectangle(s(x, y, x + 46, y + 46), radius=12 * SS, fill=c + (90,))
    d.rounded_rectangle(s(70, 470, 680, 860), radius=40 * SS, fill=CREAM_DARK)
    block_grid(d, 110, 600, 7, 3, 64, 12, seed=2)
    draw_critter(d, 250, 420, 110, (214, 160, 110), "round")
    draw_critter(d, 500, 440, 90, WHITE, "cat")
    draw_critter(d, 375, 520, 70, (250, 210, 120), "long")
    center_text(d, 690, 880, "※仮素材", 20, BROWN)
    save(img, "kv.webp", w, h)


def logo():
    w, h = 600, 220
    img, d = canvas(w, h, (0, 0, 0, 0))
    center_text(d, 300, 80, "サンプルパズル", 64, ORANGE, stroke=8, stroke_fill=WHITE)
    center_text(d, 300, 160, "〜 ことりの森 〜（仮）", 34, BROWN, stroke=6, stroke_fill=WHITE)
    save(img, "logo.webp", w, h)


def heading(name, text):
    w, h = 640, 110
    img, d = canvas(w, h, (0, 0, 0, 0))
    d.polygon([s(10, 30), s(70, 30), s(50, 55), s(70, 80), s(10, 80)], fill=TEAL)
    d.polygon([s(630, 30), s(570, 30), s(590, 55), s(570, 80), s(630, 80)], fill=TEAL)
    d.rounded_rectangle(s(55, 15, 585, 95), radius=40 * SS, fill=BROWN)
    d.rounded_rectangle(s(63, 23, 577, 87), radius=32 * SS, outline=CREAM, width=3 * SS)
    center_text(d, 320, 56, text, 38, WHITE)
    for x in (95, 545):
        d.regular_polygon((x * SS, 55 * SS, 10 * SS), 4, rotation=45, fill=ORANGE)
    save(img, name, w, h)


def reward(name, kind):
    w, h = 400, 300
    img, d = canvas(w, h, (0, 0, 0, 0))
    d.ellipse(s(60, 10, 340, 290), fill=WHITE)
    if kind == "cushion":
        d.rounded_rectangle(s(110, 90, 290, 220), radius=50 * SS, fill=PINK)
        d.rounded_rectangle(s(130, 110, 270, 200), radius=40 * SS, outline=WHITE, width=5 * SS)
    elif kind == "coin":
        d.ellipse(s(110, 60, 290, 240), fill=ORANGE)
        d.ellipse(s(135, 85, 265, 215), outline=(255, 220, 140), width=8 * SS)
        center_text(d, 200, 150, "★", 70, (255, 236, 180))
    elif kind == "outfit":
        d.polygon([s(140, 80), s(260, 80), s(300, 130), s(270, 150), s(260, 230), s(140, 230), s(130, 150), s(100, 130)], fill=TEAL)
        d.ellipse(s(180, 70, 220, 105), fill=WHITE)
        d.regular_polygon((200 * SS, 170 * SS, 22 * SS), 5, fill=ORANGE)
    save(img, name, w, h)


def screenshot(name, idx):
    w, h = 540, 960
    img, d = canvas(w, h, (255, 238, 200))
    d.rounded_rectangle(s(30, 40, 510, 150), radius=30 * SS, fill=BROWN)
    labels = ["かんたん3マッチ（仮）", "おへやをかざろう（仮）", "なかまとあつめよう（仮）"]
    center_text(d, 270, 95, labels[idx], 34, WHITE)
    if idx == 0:
        d.rounded_rectangle(s(40, 220, 500, 780), radius=30 * SS, fill=CREAM_DARK)
        block_grid(d, 62, 245, 7, 8, 52, 12, seed=idx)
        draw_critter(d, 420, 830, 80, (214, 160, 110), "round")
    elif idx == 1:
        d.rectangle(s(40, 220, 500, 620), fill=(240, 225, 255))
        d.rectangle(s(40, 620, 500, 860), fill=(222, 190, 150))
        d.rounded_rectangle(s(80, 520, 280, 650), radius=30 * SS, fill=PINK)
        d.rounded_rectangle(s(330, 300, 460, 420), radius=10 * SS, fill=WHITE, outline=BROWN, width=6 * SS)
        draw_critter(d, 380, 640, 80, WHITE, "cat")
    else:
        for i, (c, ear) in enumerate([((214, 160, 110), "round"), (WHITE, "cat"), ((250, 210, 120), "long"), (BLUE, "round")]):
            cx = 150 + (i % 2) * 240
            cy = 360 + (i // 2) * 300
            d.rounded_rectangle(s(cx - 110, cy - 130, cx + 110, cy + 130), radius=30 * SS, fill=WHITE)
            draw_critter(d, cx, cy, 70, c, ear)
    center_text(d, 270, 920, "※画面はイメージです（仮素材）", 22, BROWN)
    save(img, name, w, h)


def chara(name, color, ear):
    w, h = 400, 400
    img, d = canvas(w, h, CREAM_DARK)
    draw_critter(d, 200, 230, 120, color, ear)
    save(img, name, w, h)


def arrow(name, direction):
    w, h = 96, 96
    img, d = canvas(w, h, (0, 0, 0, 0))
    d.ellipse(s(4, 4, 92, 92), fill=WHITE, outline=BROWN, width=5 * SS)
    if direction == "left":
        d.polygon([s(30, 48), s(58, 26), s(58, 70)], fill=BROWN)
    else:
        d.polygon([s(66, 48), s(38, 26), s(38, 70)], fill=BROWN)
    save(img, name, w, h)


def badge(name, line1, line2):
    """ストアバッジの仮画像。本番は Apple / Google 公式バッジに差し替えること。"""
    w, h = 360, 108
    img, d = canvas(w, h, (0, 0, 0, 0))
    d.rounded_rectangle(s(2, 2, 358, 106), radius=18 * SS, fill=(20, 20, 20), outline=(160, 160, 160), width=2 * SS)
    center_text(d, 180, 38, line1, 22, WHITE)
    center_text(d, 180, 72, line2, 32, WHITE)
    save(img, name, w, h)


def ogp():
    w, h = 1200, 630
    img, d = canvas(w, h, CREAM)
    block_grid(d, 60, 380, 14, 2, 66, 14, seed=1)
    draw_critter(d, 220, 230, 110, (214, 160, 110), "round")
    draw_critter(d, 980, 240, 100, WHITE, "cat")
    center_text(d, 600, 170, "サンプルパズル（仮）", 72, ORANGE, stroke=8, stroke_fill=WHITE)
    center_text(d, 600, 270, "事前登録受付中！", 56, BROWN)
    save(img, "ogp.png", w, h, fmt="PNG")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    kv()
    logo()
    for n, t in [("h_reward", "事前登録報酬"), ("h_game", "ゲーム紹介"), ("h_chara", "キャラクター紹介"), ("h_sns", "公式SNSをチェック")]:
        heading(f"{n}.webp", t)
    for i, k in enumerate(["cushion", "coin", "outfit"], 1):
        reward(f"reward_{i}.webp", k)
    for i in range(3):
        screenshot(f"ss_{i + 1}.webp", i)
    for i, (c, e) in enumerate([((214, 160, 110), "round"), (WHITE, "cat"), ((250, 210, 120), "long"), (BLUE, "round")], 1):
        chara(f"chara_{i}.webp", c, e)
    arrow("arrow_left.webp", "left")
    arrow("arrow_right.webp", "right")
    badge("badge_appstore.webp", "仮バッジ", "App Store")
    badge("badge_googleplay.webp", "仮バッジ", "Google Play")
    ogp()


if __name__ == "__main__":
    main()
