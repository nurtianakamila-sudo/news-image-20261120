"""News front page for Friday 20 November 2026, drawn from scratch with PIL.

Writes one 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png.
Offline, deterministic: no time, no randomness, no network.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
TEAL = (46, 111, 122)
SKY = (168, 205, 219)
SAND = (232, 214, 178)
GREEN = (74, 124, 72)
GOLD = (212, 175, 55)
GREY = (90, 90, 90)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def font(size, bold=True):
    for path in FONT_PATHS:
        if ("Bold" in path) == bold and os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, width, text, fnt, fill=INK, leading=None, align="left"):
    lines = wrap(draw, text, fnt, width)
    step = leading or int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += step
    return y


def cyclone_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.polygon([(x0 + 190, y0), (x1, y0), (x1, y1), (x0 + 60, y1),
               (x0 + 90, y0 + 180), (x0 + 150, y0 + 90)], fill=SAND)
    d.line([(x0 + 190, y0), (x0 + 150, y0 + 90), (x0 + 90, y0 + 180),
            (x0 + 60, y1)], fill=(120, 100, 70), width=3)
    cx, cy = x0 + 330, y0 + 128
    for r, col in ((120, (255, 255, 255)), (94, (220, 235, 240)),
                   (68, (255, 255, 255)), (42, (200, 225, 235)),
                   (20, (255, 255, 255))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=7)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=NAVY)
    d.ellipse([x0 + 205, y0 + 235, x0 + 221, y0 + 251], fill=RED)
    d.text((x0 + 232, y0 + 228), "GOPALPUR", font=font(20), fill=RED)
    d.text((x0 + 16, y0 + 14), "BAY OF BENGAL", font=font(18, bold=False),
           fill=(60, 90, 110))
    d.text((x0 + 16, y1 - 34), "ODISHA, INDIA", font=font(18, bold=False),
           fill=(90, 75, 50))


def whitehouse_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    bx, by = x0 + 55, y0 + 78
    d.rectangle([bx, by, bx + 190, by + 52], fill=(240, 240, 235))
    for i in range(6):
        px = bx + 14 + i * 30
        d.rectangle([px, by + 8, px + 12, by + 52], fill=(200, 200, 190))
    d.rectangle([bx + 70, by - 26, bx + 120, by], fill=(240, 240, 235))
    d.pieslice([bx + 70, by - 52, bx + 120, by], 180, 360, fill=(240, 240, 235))
    d.rectangle([bx - 18, by + 52, bx + 208, by + 60], fill=(220, 220, 210))
    for sx in (x0 + 22, x1 - 34):
        d.rectangle([sx, y0 + 96, sx + 12, y0 + 130], fill=(150, 150, 140))
        d.ellipse([sx - 8, y0 + 82, sx + 20, y0 + 100], fill=(120, 160, 110))
    d.text((x0 + 16, y0 + 10), "WASHINGTON, D.C.", font=font(16, bold=False),
           fill=(200, 210, 225))


def eu_uk_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(35, 62, 130))
    cx, cy = x0 + 150, y0 + 78
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + 52 * math.cos(a), cy + 52 * math.sin(a)
        d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=GOLD)
    d.rectangle([x0 + 205, y0 + 28, x1 - 18, y0 + 128], fill=(200, 200, 205))
    d.line([(x0 + 205, y0 + 78), (x1 - 18, y0 + 78)], fill=RED, width=14)
    d.line([(x0 + 250, y0 + 28), (x0 + 250, y0 + 128)], fill=RED, width=14)
    d.line([(x0 + 205, y0 + 28), (x1 - 18, y0 + 128)], fill=RED, width=7)
    d.line([(x1 - 18, y0 + 28), (x0 + 205, y0 + 128)], fill=RED, width=7)
    d.text((x0 + 16, y0 + 10), "BRUSSELS", font=font(16, bold=False),
           fill=(200, 210, 235))


def cricket_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=GREEN)
    d.rectangle([x0, y0 + 96, x1, y1], fill=(222, 200, 150))
    for i in range(3):
        sx = x0 + 130 + i * 14
        d.rectangle([sx, y0 + 66, sx + 7, y0 + 98], fill=(245, 240, 220))
    d.ellipse([x0 + 250, y0 + 108, x0 + 266, y0 + 124], fill=RED)
    d.line([(x0 + 30, y0 + 118), (x0 + 90, y0 + 62)], fill=(190, 150, 90),
           width=12)
    d.text((x0 + 16, y0 + 10), "BASIN RESERVE", font=font(16, bold=False),
           fill=(220, 235, 220))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28
    d.line([(m, 18), (W - m, 18)], fill=INK, width=3)
    d.text((W / 2, 30), "WORLD NEWS", font=font(66), fill=INK, anchor="ma")
    d.line([(m, 108), (W - m, 108)], fill=INK, width=3)
    d.text((W / 2, 118), "FRIDAY, 20 NOVEMBER 2026", font=font(24),
           fill=RED, anchor="ma")
    d.line([(m, 152), (W - m, 152)], fill=INK, width=1)

    # Lead story: Cyclone Akvan.
    ly0, ly1 = 168, 606
    cyclone_art(d, m, ly0, W - m, ly0 + 252)
    y = ly0 + 266
    d.text((m, y), "CYCLONE AKVAN  •  INDIA", font=font(22), fill=RED)
    y += 34
    y = text_block(d, m, y, W - 2 * m,
                   "CYCLONE AKVAN CLOSES IN ON INDIA'S COAST",
                   font(40), leading=46)
    y += 6
    text_block(d, m, y, W - 2 * m,
               "Landfall due at noon near Gopalpur, Odisha — 105,000 people "
               "moved to shelters as winds reach 110 km/h.",
               font(22, bold=False), leading=28)

    d.line([(m, 622), (W - m, 622)], fill=INK, width=2)

    # Three smaller stories.
    cols = [
        ("WHITE HOUSE", "TRUMP TO BRIEF PRESS AT NOON",
         "President to hail his China trip and tout Thailand and "
         "Philippines trade deals at the White House.", whitehouse_art),
        ("EUROPE", "EU AND UK SUMMIT IN BRUSSELS",
         "Costa and von der Leyen welcome PM Burnham for talks on "
         "security and trade.", eu_uk_art),
        ("CRICKET  •  WELLINGTON", "NICHOLLS 146* AS NZ PILE ON",
         "New Zealand 317 for 6 at lunch on day two; Phillips hits a "
         "century in a 216-run stand.", cricket_art),
    ]
    cw = (W - 2 * m - 2 * 16) // 3
    for i, (kicker, head, deck, art) in enumerate(cols):
        x0 = m + i * (cw + 16)
        x1 = x0 + cw
        art(d, x0, 640, x1, 790)
        y = 802
        d.text((x0, y), kicker, font=font(17), fill=RED)
        y += 26
        y = text_block(d, x0, y, cw, head, font(25), leading=29)
        y += 4
        text_block(d, x0, y, cw, deck, font(18, bold=False), leading=23)

    d.line([(m, 968), (W - m, 968)], fill=INK, width=1)
    d.text((W / 2, 976),
           "Sources: India Meteorological Department  •  Reuters  •  "
           "European Council  •  Truth Social",
           font=font(14, bold=False), fill=GREY, anchor="ma")
    return img


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out, exist_ok=True)
    img = build()
    path = os.path.join(out, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
