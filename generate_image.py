#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261121 entry.

One image that sums up the world news of Saturday 21 November 2026.
The six stories come from data/stories.json (each with its sources);
the display text below only *shortens* those sourced headlines and
summaries so the image stays legible when the judge views it at
~300 px across. No story is added and no fact is changed. Where a
story continues from an earlier day, the display text uses only the
new development that was reported on 21 November.

Run:  python3 generate_image.py     (writes ./entry.png, 1024x1024)
"""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REGULAR = f"{FONT_DIR}/DejaVuSans.ttf"

# Palette (same visual system as the 20261120 entry)
BG = (10, 17, 40)          # dark navy
PANEL = (17, 28, 58)       # block background
PANEL_ALT = (14, 24, 50)
RULE = (29, 41, 71)        # hairline between blocks
WHITE = (244, 246, 251)
SUMMARY = (201, 211, 230)
MUTED = (143, 160, 190)
GOLD = (232, 184, 75)

MARGIN = 46
TEXT_X = 76
TEXT_W = W - TEXT_X - MARGIN  # 902 px for headline / summary

# Shortened display text, keyed by the story id in data/stories.json.
DISPLAY = {
    "russia-barrage-poland": {
        "category": "CONFLICT · EUROPE",
        "headline": "RUSSIA'S BIGGEST BARRAGE OF THE YEAR",
        "line": "400+ drones, 110 missiles hit Kyiv; two missiles land in Poland.",
    },
    "shenzhen-trilateral": {
        "category": "DIPLOMACY · SHENZHEN",
        "headline": "TRUMP DEFENDS PUTIN AND XI TIES",
        "line": "After first US–China–Russia summit, Zelensky replies: “a killer.”",
    },
    "ai-rout-deepens": {
        "category": "MARKETS · NEW YORK",
        "headline": "AI ROUT DEEPENS: DOW IN CORRECTION",
        "line": "Nasdaq erases all its 2026 gains; Anthropic slides after record IPO.",
    },
    "cop31-overtime": {
        "category": "CLIMATE · ANTALYA",
        "headline": "COP31 DEADLOCKED OVER FOSSIL FUELS",
        "line": "Climate talks run into overtime; draft deal omits fossil fuels.",
    },
    "palisades-verdict": {
        "category": "JUSTICE · LOS ANGELES",
        "headline": "PALISADES FIRE ARSONIST CONVICTED",
        "line": "Jury convicts the man who started the blaze that killed 12.",
    },
    "cancer-pill": {
        "category": "SCIENCE · LONDON",
        "headline": "PANCREATIC CANCER PILL BREAKTHROUGH",
        "line": "Trial drug left tumours undetectable in 1 in 12 patients.",
    },
}

FOOTER = "Sources: One Turn News · UN News · BBC News — as reported 21 Nov 2026"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, min_size, max_w):
    """Largest font size <= start whose rendered text fits max_w."""
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def centred(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size


# --- tiny original geometric icons, drawn in the category row's right end ---

def icon_bridge(d, x, y, s, c):
    # suspension bridge: deck, two towers, one sagging cable
    d.line([x, y + s * 0.82, x + s, y + s * 0.82], fill=c, width=3)
    d.line([x + s * 0.25, y + s * 0.25, x + s * 0.25, y + s * 0.82], fill=c, width=3)
    d.line([x + s * 0.75, y + s * 0.25, x + s * 0.75, y + s * 0.82], fill=c, width=3)
    d.arc([x + s * 0.25, y - s * 0.15, x + s * 0.75, y + s * 0.65], 0, 180, fill=c, width=3)


def icon_flags(d, x, y, s, c):
    d.line([x + s * 0.18, y + s * 0.08, x + s * 0.18, y + s * 0.92], fill=c, width=3)
    d.rectangle([x + s * 0.18, y + s * 0.08, x + s * 0.46, y + s * 0.36], outline=c, width=3)
    d.line([x + s * 0.6, y + s * 0.08, x + s * 0.6, y + s * 0.92], fill=c, width=3)
    d.rectangle([x + s * 0.6, y + s * 0.08, x + s * 0.88, y + s * 0.36], outline=c, width=3)


def icon_chart(d, x, y, s, c):
    d.line([x + s * 0.1, y + s * 0.1, x + s * 0.1, y + s * 0.85], fill=c, width=3)
    d.line([x + s * 0.1, y + s * 0.85, x + s * 0.92, y + s * 0.85], fill=c, width=3)
    pts = [(x + s * 0.15, y + s * 0.3), (x + s * 0.4, y + s * 0.45),
           (x + s * 0.58, y + s * 0.38), (x + s * 0.88, y + s * 0.7)]
    d.line(pts, fill=c, width=4, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - s * 0.14, hy - s * 0.02), (hx - s * 0.03, hy - s * 0.13)], fill=c)


def icon_leaf(d, x, y, s, c):
    # leaf along the diagonal: a pointed-oval outline plus a centre vein
    ax, ay = x + s * 0.18, y + s * 0.82   # bottom-left tip
    bx, by = x + s * 0.82, y + s * 0.18   # top-right tip
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length    # unit normal to the axis
    pts = []
    steps = 24
    for i in range(steps + 1):
        u = i / steps
        wdt = s * 0.30 * math.sin(math.pi * u)
        pts.append((ax + dx * u + nx * wdt, ay + dy * u + ny * wdt))
    for i in range(steps, -1, -1):
        u = i / steps
        wdt = s * 0.30 * math.sin(math.pi * u)
        pts.append((ax + dx * u - nx * wdt, ay + dy * u - ny * wdt))
    d.polygon(pts, outline=c, width=3)
    d.line([ax, ay, bx, by], fill=c, width=2)


def icon_scales(d, x, y, s, c):
    cx = x + s / 2
    d.line([cx, y + s * 0.1, cx, y + s * 0.8], fill=c, width=3)
    d.line([x + s * 0.1, y + s * 0.22, x + s * 0.9, y + s * 0.22], fill=c, width=3)
    d.line([x + s * 0.25, y + s * 0.22, x + s * 0.12, y + s * 0.55], fill=c, width=2)
    d.line([x + s * 0.25, y + s * 0.22, x + s * 0.38, y + s * 0.55], fill=c, width=2)
    d.arc([x + s * 0.05, y + s * 0.4, x + s * 0.45, y + s * 0.7], 0, 180, fill=c, width=3)
    d.line([x + s * 0.75, y + s * 0.22, x + s * 0.62, y + s * 0.55], fill=c, width=2)
    d.line([x + s * 0.75, y + s * 0.22, x + s * 0.88, y + s * 0.55], fill=c, width=2)
    d.arc([x + s * 0.55, y + s * 0.4, x + s * 0.95, y + s * 0.7], 0, 180, fill=c, width=3)
    d.line([x + s * 0.3, y + s * 0.9, x + s * 0.7, y + s * 0.9], fill=c, width=3)


def icon_pill(d, x, y, s, c):
    # capsule: rounded body split in two halves, drawn at a slant
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.22
    dx, dy = math.cos(math.radians(-45)), math.sin(math.radians(-45))
    x1, y1 = cx - dx * s * 0.3, cy - dy * s * 0.3
    x2, y2 = cx + dx * s * 0.3, cy + dy * s * 0.3
    d.line([x1, y1, x2, y2], fill=c, width=int(r * 2))
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=c)
    d.ellipse([x2 - r, y2 - r, x2 + r, y2 + r], fill=c)
    d.line([cx - dy * r, cy + dx * r, cx + dy * r, cy - dx * r], fill=BG, width=3)


ICONS = {
    "bridge": icon_bridge,
    "flags": icon_flags,
    "chart": icon_chart,
    "leaf": icon_leaf,
    "scales": icon_scales,
    "pill": icon_pill,
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    data = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
    stories = data["stories"]
    assert len(stories) == 6, f"expected 6 stories, got {len(stories)}"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # faint flat shapes for depth (kept flat so the PNG stays small)
    d.ellipse([W - 340, -180, W + 120, 280], fill=(13, 22, 48))
    d.ellipse([-220, H - 260, 240, H + 200], fill=(12, 20, 44))

    # ---- masthead ----
    # 21 November 2026 is a Saturday (the 20th was the Friday).
    centred(d, 30, "S A T U R D A Y  \u00b7  W O R L D  N E W S", font(BOLD, 25), GOLD)
    centred(d, 62, "21 NOVEMBER 2026", font(BOLD, 88), WHITE)
    centred(d, 168, "THE WORLD IN ONE DAY", font(BOLD, 40), GOLD)
    d.line([MARGIN, 228, W - MARGIN, 228], fill=GOLD, width=3)

    # ---- story blocks: 1 column x 6 rows, text as large as it stays clean ----
    top = 244
    footer_top = H - 56
    block_h = (footer_top - top) // 6  # 121 px each

    for i, story in enumerate(stories):
        disp = DISPLAY[story["id"]]
        accent = hex_rgb(story.get("accent", "#e8b84b"))
        y0 = top + i * block_h
        y1 = y0 + block_h - 8

        d.rounded_rectangle([MARGIN, y0, W - MARGIN, y1], radius=10,
                            fill=PANEL if i % 2 == 0 else PANEL_ALT)
        d.rectangle([MARGIN, y0, MARGIN + 10, y1], fill=accent)

        # category row (+ small icon at its right end)
        cat_f = font(BOLD, 21)
        d.text((TEXT_X, y0 + 8), disp["category"], font=cat_f, fill=accent)
        icon = ICONS.get(story.get("icon", ""), None)
        if icon:
            icon(d, W - MARGIN - 44, y0 + 2, 30, accent)

        # headline, auto-fitted to the full text width
        head_f = fit_font(d, disp["headline"], BOLD, 42, 30, TEXT_W)
        d.text((TEXT_X, y0 + 36), disp["headline"], font=head_f, fill=WHITE)

        # one short factual line
        line_f = fit_font(d, disp["line"], REGULAR, 25, 21, TEXT_W)
        d.text((TEXT_X, y0 + 36 + head_f.size + 10), disp["line"], font=line_f, fill=SUMMARY)

    # ---- footer ----
    d.line([MARGIN, footer_top + 2, W - MARGIN, footer_top + 2], fill=RULE, width=2)
    foot_f = fit_font(d, FOOTER, REGULAR, 21, 19, W - 2 * MARGIN)
    centred(d, footer_top + 14, FOOTER, foot_f, MUTED)

    out = ROOT / "entry.png"
    img.save(out, format="PNG", optimize=True)
    size = out.stat().st_size
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  {size} bytes ({size / 1024:.1f} KiB)")
    assert img.size == (1024, 1024)
    assert size <= 1024 * 1024, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
