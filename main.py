#!/usr/bin/env python3
"""News Image - 20 November 2026 (v2, written fresh).

Draws a 1024x1024 front-page PNG summing up 20 November 2026 world news.
Stdlib + Pillow only, offline, deterministic. No system fonts are used:
text comes from PIL's bundled default font via ImageFont.load_default(size=...),
with a plain load_default() fallback. Text is centred manually with
textlength measurements - no Pillow text-anchor feature is used anywhere.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)      # warm newsprint
INK = (22, 30, 46)           # near-black navy
NAVY = (22, 35, 63)
NAVY_LT = (38, 56, 92)
RED = (176, 42, 48)
GOLD = (198, 148, 52)
SEA = (126, 178, 205)
SEA_DK = (74, 124, 158)
LAND = (232, 214, 176)
LAND_DK = (206, 178, 132)
TEAL = (18, 110, 118)
GREY = (96, 100, 110)
RULE = (180, 175, 160)
WHITE = (255, 255, 255)
CREAM = (255, 250, 238)

# ---------------------------------------------------------------- fonts
def font(size):
    """Bundled default font at the requested size; plain fallback if needed."""
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


F_MAST = font(58)
F_DATE = font(19)
F_KICK = font(17)
F_HEAD = font(44)
F_HEAD2 = font(34)
F_SUB = font(19)
F_BODY = font(18)
F_BODY_SM = font(16)
F_PANEL_H = font(23)
F_PANEL_B = font(16)
F_NUM = font(30)
F_NUM_LBL = font(14)
F_FOOT = font(13)
F_TAG = font(15)

# ---------------------------------------------------------------- helpers
def cx(d, cx, y, s, f, fill):
    """Draw text centred on x=cx (manual centring via textlength)."""
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)


def rx(d, right, y, s, f, fill):
    """Draw text right-aligned to x=right."""
    w = d.textlength(s, font=f)
    d.text((right - w, y), s, font=f, fill=fill)


def wrap(d, text, f, width):
    """Greedy word wrap measured with textlength."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, width, fill=INK, leading=7):
    """Draw a wrapped paragraph; return the y just below the last line."""
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + leading
    return y


def rule(d, x0, x1, y, fill=RULE, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- cyclone art
def draw_cyclone(d, x0, y0, x1, y1):
    """Stylised cyclone spiral over a coastline, drawn with arcs and lines."""
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=INK, width=2)
    # land mass on the right third
    d.polygon([(x0 + (x1 - x0) * 0.62, y0),
               (x1, y0), (x1, y1),
               (x0 + (x1 - x0) * 0.58, y1),
               (x0 + (x1 - x0) * 0.66, y0 + (y1 - y0) * 0.55)],
              fill=LAND)
    d.line([(x0 + (x1 - x0) * 0.62, y0),
            (x0 + (x1 - x0) * 0.66, y0 + (y1 - y0) * 0.55),
            (x0 + (x1 - x0) * 0.58, y1)], fill=LAND_DK, width=2)
    # spiral: concentric broken arcs, white with navy outline feel
    cx0, cy0 = x0 + (x1 - x0) * 0.42, y0 + (y1 - y0) * 0.52
    for r, start, end, col, wd in [
            (68, 20, 300, WHITE, 7), (68, 20, 300, NAVY, 2),
            (52, 140, 420, WHITE, 7), (52, 140, 420, NAVY, 2),
            (36, 260, 540, WHITE, 7), (36, 260, 540, NAVY, 2),
            (20, 40, 320, WHITE, 7), (20, 40, 320, NAVY, 2)]:
        d.arc([cx0 - r, cy0 - r, cx0 + r, cy0 + r], start, end,
              fill=col, width=wd)
    d.ellipse([cx0 - 9, cy0 - 9, cx0 + 9, cy0 + 9], fill=NAVY)
    # rain streaks over the land
    for i in range(14):
        rx0 = x0 + (x1 - x0) * 0.68 + i * 9
        ry0 = y0 + 12 + (i % 4) * 16
        d.line([(rx0, ry0), (rx0 - 6, ry0 + 16)], fill=SEA_DK, width=2)
    # Gopalpur marker
    gx, gy = x0 + (x1 - x0) * 0.63, y0 + (y1 - y0) * 0.52
    d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=RED, outline=WHITE, width=2)
    d.text((gx + 12, gy - 8), "GOPALPUR", font=F_TAG, fill=INK)
    d.text((x0 + 10, y1 - 24), "BAY OF BENGAL", font=F_TAG, fill=NAVY_LT)


# ---------------------------------------------------------------- flag strips
def draw_flags_trump(d, x, y, w, h):
    """Three small flag chips: US, China, Russia."""
    cw = w // 3
    # US: red/white stripes + blue canton
    d.rectangle([x, y, x + cw - 8, y + h], fill=WHITE, outline=INK, width=1)
    for i in range(4):
        d.rectangle([x, y + i * (h // 4), x + cw - 8, y + (i + 1) * (h // 4)],
                    fill=RED if i % 2 == 0 else WHITE)
    d.rectangle([x, y, x + (cw - 8) // 2, y + h // 2], fill=NAVY)
    # China: red field, yellow stars
    d.rectangle([x + cw, y, x + 2 * cw - 8, y + h], fill=(222, 41, 16),
                outline=INK, width=1)
    d.ellipse([x + cw + 6, y + 5, x + cw + 16, y + 15], fill=GOLD)
    d.ellipse([x + cw + 20, y + 4, x + cw + 26, y + 10], fill=GOLD)
    d.ellipse([x + cw + 22, y + 14, x + cw + 28, y + 20], fill=GOLD)
    # Russia: white / blue / red tricolour
    d.rectangle([x + 2 * cw, y, x + 3 * cw - 8, y + h], fill=WHITE,
                outline=INK, width=1)
    d.rectangle([x + 2 * cw, y + h // 3, x + 3 * cw - 8, y + 2 * h // 3],
                fill=(0, 57, 166))
    d.rectangle([x + 2 * cw, y + 2 * h // 3, x + 3 * cw - 8, y + h],
                fill=(213, 0, 50))


def draw_flags_euuk(d, x, y, w, h):
    """EU circle-of-stars chip and a simplified Union Jack chip."""
    cw = w // 2
    d.rectangle([x, y, x + cw - 8, y + h], fill=(0, 51, 153),
                outline=INK, width=1)
    import math
    ccx, ccy = x + (cw - 8) // 2, y + h // 2
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = ccx + int(13 * math.cos(a)) - 2
        sy = ccy + int(13 * math.sin(a)) - 2
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=GOLD)
    d.rectangle([x + cw, y, x + 2 * cw - 8, y + h], fill=(1, 33, 105),
                outline=INK, width=1)
    d.rectangle([x + cw, y + h // 2 - 4, x + 2 * cw - 8, y + h // 2 + 4],
                fill=WHITE)
    d.rectangle([x + cw + (cw - 8) // 2 - 4, y, x + cw + (cw - 8) // 2 + 4,
                 y + h], fill=WHITE)
    d.rectangle([x + cw, y + h // 2 - 2, x + 2 * cw - 8, y + h // 2 + 2],
                fill=RED)
    d.rectangle([x + cw + (cw - 8) // 2 - 2, y, x + cw + (cw - 8) // 2 + 2,
                 y + h], fill=RED)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 118], fill=RED)
    cx(d, W // 2, 14, "THE WORLD TODAY", F_MAST, WHITE)
    cx(d, W // 2, 82, "FRIDAY  ·  20 NOVEMBER 2026  ·  ONE DAY, ONE IMAGE",
       F_DATE, (200, 205, 220))
    rx(d, W - M, 20, "No. 324", F_DATE, GOLD)
    d.text((M, 20), "EST. 2026", font=F_DATE, fill=GOLD)

    # ---- lead story ----------------------------------------------------
    y = 138
    d.text((M, y), "LEAD STORY - INDIA", font=F_KICK, fill=RED)
    y += 26
    d.text((M, y), "AKVAN COMES ASHORE", font=F_HEAD, fill=INK)
    y += 52
    d.text((M, y), "Weaker than feared, but the rain goes on", font=F_SUB, fill=NAVY_LT)
    y += 30

    # illustration, left column
    art_x0, art_y0, art_x1, art_y1 = M, y, 648, y + 148
    draw_cyclone(d, art_x0, art_y0, art_x1, art_y1)
    y = art_y1 + 14

    lead_body = (
        "Cyclone Akvan crossed the north Andhra Pradesh and south Odisha "
        "coast near Gopalpur between 7.30 and 8.30 this morning, the India "
        "Meteorological Department said, with winds of 70-80 kmph gusting "
        "to 90 kmph. The storm had weakened overnight from a severe "
        "cyclonic storm."
    )
    y = para(d, M, y, lead_body, F_BODY, 620, leading=5)
    y += 4
    lead_body2 = (
        "No major damage or loss of life had been reported by midday, "
        "Disaster Management Minister Suresh Pujari said. Odisha had moved "
        "2,98,676 people to 2,523 relief camps, with 423 rescue teams "
        "deployed and 9,341 shelters ready. Ganjam recorded up to 209 mm "
        "of rain."
    )
    y = para(d, M, y, lead_body2, F_BODY, 620, leading=6)

    # ---- numbers box, right column --------------------------------------
    bx0, bx1 = 668, W - M
    by0, by1 = 138, 596
    d.rectangle([bx0, by0, bx1, by1], fill=CREAM, outline=INK, width=2)
    d.rectangle([bx0, by0, bx1, by0 + 40], fill=NAVY)
    cx(d, (bx0 + bx1) // 2, by0 + 9, "THE DAY IN NUMBERS", F_KICK, WHITE)
    stats = [
        ("2,98,676", "people evacuated in Odisha"),
        ("423", "rescue teams deployed"),
        ("209 mm", "rain in Ganjam district"),
        ("100,000", "youth places a year, UK-EU deal"),
        ("90 min", "Trump-Xi-Putin summit"),
    ]
    sy = by0 + 56
    for i, (num, lbl) in enumerate(stats):
        d.text((bx0 + 16, sy), num, font=F_NUM, fill=RED)
        ly = sy + 38
        for ln in wrap(d, lbl, F_NUM_LBL, bx1 - bx0 - 32):
            d.text((bx0 + 16, ly), ln, font=F_NUM_LBL, fill=GREY)
            ly += 17
        sy = ly + 10
        if i < len(stats) - 1:
            rule(d, bx0 + 16, bx1 - 16, sy)
            sy += 12

    # ---- three supporting panels ----------------------------------------
    py0, py1 = 622, 936
    pw = (W - 2 * M - 2 * 16) // 3
    panels = [
        {
            "kick": "WASHINGTON  ·  SHENZHEN",
            "head": "A '12 out of 10' summit",
            "art": "trump",
            "body": ("Trump, Xi and Putin signed a joint 'Declaration on "
                     "Peace' after a 90-minute trilateral in Shenzhen: UN "
                     "reform, more fuel supplies, and a pledge that nuclear "
                     "war 'cannot be won and must never be fought'. No "
                     "mention of Ukraine; no arms-control talks. Trump "
                     "rates it 'a 12' and briefs reporters at noon ET today."),
        },
        {
            "kick": "BRUSSELS",
            "head": "Britain-EU reset agreed",
            "art": "euuk",
            "body": ("Britain and the EU are set to agree a reset deal at "
                     "today's summit in Brussels: a youth mobility scheme "
                     "for up to 100,000 young people a year, for up to "
                     "three years; food-trade checks scrapped, worth up to "
                     "5.1bn pounds a year; and linked carbon markets. "
                     "Tuition fees are unresolved; the deal takes force "
                     "from 1 March 2028."),
        },
        {
            "kick": "IN BRIEF",
            "head": "Also today",
            "art": None,
            "body": ("69 trains cancelled across the east coast as Akvan "
                     "moved inland. Schools shut in 13 Odisha districts. "
                     "1,317 babies were delivered in shelters and "
                     "hospitals before landfall. Akvan is the third "
                     "cyclone to threaten Odisha in 24 days. Heavy rain is "
                     "forecast for West Bengal, Jharkhand and Bihar "
                     "tomorrow."),
        },
    ]
    for i, p in enumerate(panels):
        px0 = M + i * (pw + 16)
        px1 = px0 + pw
        d.rectangle([px0, py0, px1, py1], fill=WHITE, outline=INK, width=2)
        d.rectangle([px0, py0, px1, py0 + 6], fill=RED)
        d.text((px0 + 14, py0 + 16), p["kick"], font=F_KICK, fill=RED)
        hy = py0 + 42
        for ln in wrap(d, p["head"], F_PANEL_H, pw - 28):
            d.text((px0 + 14, hy), ln, font=F_PANEL_H, fill=INK)
            hy += F_PANEL_H.size + 4
        hy += 6
        if p["art"] == "trump":
            draw_flags_trump(d, px0 + 14, hy, pw - 28, 34)
            hy += 46
        elif p["art"] == "euuk":
            draw_flags_euuk(d, px0 + 14, hy, pw - 28, 34)
            hy += 46
        para(d, px0 + 14, hy, p["body"], F_PANEL_B, pw - 28, leading=5)

    # ---- footer ---------------------------------------------------------
    fy = 956
    rule(d, M, W - M, fy)
    cx(d, W // 2, fy + 10,
       "Sources: India Meteorological Department; The Hindu BusinessLine; Reuters; BBC; GOV.UK - 20 November 2026",
       F_FOOT, GREY)
    cx(d, W // 2, fy + 30,
       "All stories verified against reporting dated 20 November 2026. The noon ET press conference had not yet taken place at press time.",
       F_FOOT, GREY)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, img.size, img.mode)


if __name__ == "__main__":
    main()
