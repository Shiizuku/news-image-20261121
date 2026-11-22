#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news broadsheet (1024x823 PNG).

One image that sums up Saturday 21 November 2026: six verified stories,
each drawn with simple PIL shapes and a short headline + caption.
Runs offline with the standard library + Pillow (build time only).
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 823
PAPER = (247, 243, 234)
INK = (24, 24, 24)
RULE = (24, 24, 24)
RED = (178, 34, 34)
BLUE = (31, 78, 121)
TEAL = (0, 102, 102)
GOLD = (184, 134, 11)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit a pixel width."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=4):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def panel(draw, box, kicker, kcolor):
    """A bordered story panel; returns the inner (x, y, w) for content."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 26], fill=kcolor)
    draw.text((x0 + 10, y0 + 5), kicker, font=font(SANS_B, 13),
              fill=(255, 255, 255))
    return x0 + 12, y0 + 34, x1 - x0 - 24


def headline(draw, x, y, w, text, size=18):
    fnt = font(SERIF_B, size)
    return para(draw, (x, y), text, fnt, INK, w, leading=2)


def caption(draw, x, y, w, text, size=12):
    return para(draw, (x, y), text, font(SANS, size), (60, 60, 60), w,
                leading=3)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
                 outline=INK, width=3)
    for k in (-0.55, 0, 0.55):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 90 + k * 90, 270 + k * 90,
                 fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - r * 0.35, cx + r, cy + r * 0.35],
                 outline=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)


def draw_burst(draw, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color, outline=INK)


def draw_chart(draw, x0, y0, x1, y1):
    pts = [(x0, y0 + 8), (x0 + 40, y0 + 24), (x0 + 80, y0 + 18),
           (x0 + 120, y0 + 44), (x0 + 160, y0 + 60), (x1, y1 - 6)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x1, y1 - 6), (x1 - 16, y1 - 16), (x1 - 14, y1)],
                 fill=RED)


def draw_quake(draw, x0, y0, x1, y1):
    draw.polygon([(x0, y1), (x0 + 45, y0 + 16), (x0 + 90, y1)],
                 fill=(139, 90, 43))
    draw.polygon([(x0 + 70, y1), (x0 + 130, y0 + 4), (x0 + 190, y1)],
                 fill=(101, 67, 50))
    mid = (y0 + y1) // 2
    pts = [(x0, mid)]
    for i, d in enumerate([0, -22, 18, -12, 24, -7, 0]):
        pts.append((x0 + 28 * (i + 1), mid + d))
    draw.line(pts, fill=RED, width=4, joint="curve")


def draw_space(draw, cx, cy):
    # Mercury with a thin orbit ring and a small spacecraft on the ring.
    draw.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(150, 150, 150),
                 outline=INK, width=2)
    for ox, oy, r in [(-14, -12, 6), (9, 6, 9), (15, -15, 4)]:
        draw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                     fill=(110, 110, 110))
    draw.ellipse([cx - 62, cy - 44, cx + 62, cy + 44], outline=GOLD, width=2)
    draw.rectangle([cx + 40, cy - 38, cx + 58, cy - 30], fill=TEAL,
                   outline=INK)
    draw.rectangle([cx + 48, cy - 34, cx + 52, cy - 16], fill=(220, 220, 220),
                   outline=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=(255, 255, 255))
    d.line([0, 118, W, 118], fill=RULE, width=3)
    d.text((24, 14), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 52), fill=INK)
    d.text((24, 78), "SATURDAY  21  NOVEMBER  2026",
           font=font(SANS_B, 24), fill=RED)
    d.text((W - 24, 82), "Six stories  •  One day",
           font=font(SANS, 18), fill=(90, 90, 90), anchor="ra")

    # ---- lead story: COP31 ----
    lx0, ly0, lx1, ly1 = 24, 132, 1000, 352
    d.rectangle([lx0, ly0, lx1, ly1], fill=(255, 255, 255), outline=INK,
                width=2)
    d.rectangle([lx0, ly0, lx1, ly0 + 28], fill=BLUE)
    d.text((lx0 + 12, ly0 + 5), "CLIMATE  •  ANTALYA, TURKEY",
           font=font(SANS_B, 14), fill=(255, 255, 255))
    draw_globe(d, lx0 + 105, ly0 + 140, 72)
    # clock showing overtime
    d.ellipse([lx0 + 205, ly0 + 92, lx0 + 253, ly0 + 140], fill=(255, 255, 255),
              outline=INK, width=3)
    d.line([lx0 + 229, ly0 + 116, lx0 + 229, ly0 + 98], fill=INK, width=3)
    d.line([lx0 + 229, ly0 + 116, lx0 + 245, ly0 + 122], fill=INK, width=3)
    d.text((lx0 + 196, ly0 + 148), "OVERTIME", font=font(SANS_B, 13),
           fill=RED)
    hx = lx0 + 280
    headline(d, hx, ly0 + 44, lx1 - hx - 16,
             "COP31 talks run into overtime with no deal in sight", size=26)
    caption(d, hx, ly0 + 128, lx1 - hx - 16,
            "Negotiators in Antalya miss their Friday deadline as nearly 200 "
            "countries split over fossil fuels and climate finance. The draft "
            "deal drops any mention of ending fossil-fuel use — and the "
            "$120bn adaptation fund.", size=15)

    # ---- grid of five stories + one numbers panel ----
    cols = [24, 352, 680]
    rows = [364, 576]
    cw, ch = 320, 200
    stories = [
        ("WAR  •  UKRAINE", RED, "blast",
         "Russian strike hits Zelenskyy's hometown",
         "Ballistic missiles hit Kryvyi Rih in a double-tap attack: 2 killed, "
         "60 wounded."),
        ("JUSTICE  •  MEXICO", TEAL, "bars",
         "Mexico captures 'El Chapo Isidro'",
         "Forces seize FBI most-wanted boss Fausto Isidro Meza Flores in "
         "Sinaloa."),
        ("MARKETS  •  NEW YORK", RED, "chart",
         "AI sell-off drags world markets down",
         "The S&P 500 falls 3.7% and Japan's Nikkei 5.1% on AI spending fears."),
        ("DISASTER  •  PERU", (139, 90, 43), "quake",
         "M6.9 quake shakes Peru's Andes",
         "The tremor, felt in Lima, strikes near Junin 108 km deep. "
         "No casualties."),
        ("SPACE  •  MERCURY", BLUE, "space",
         "BepiColombo reaches Mercury",
         "After eight years, the ESA/JAXA craft enters orbit around Mercury."),
    ]
    for i, (kick, col, kind, head, cap) in enumerate(stories):
        x0 = cols[i % 3]
        y0 = rows[i // 3]
        x, y, w = panel(d, (x0, y0, x0 + cw, y0 + ch), kick, col)
        pic_y1 = y + 96
        if kind == "blast":
            for bx in (x + 30, x + 90, x + 150):
                d.rectangle([bx, y + 56, bx + 42, y + 88], fill=(70, 70, 70))
            draw_burst(d, x + 105, y + 34, 32, (255, 176, 0))
            draw_burst(d, x + 105, y + 34, 15, (255, 90, 0))
        elif kind == "bars":
            for bx in range(x + 20, x + 210, 26):
                d.line([bx, y + 6, bx, y + 78], fill=(120, 120, 120), width=7)
            d.ellipse([x + 82, y + 62, x + 112, y + 88], outline=INK, width=4)
            d.ellipse([x + 122, y + 62, x + 152, y + 88], outline=INK,
                      width=4)
            d.line([x + 112, y + 77, x + 122, y + 77], fill=INK, width=4)
        elif kind == "chart":
            draw_chart(d, x + 10, y + 8, x + 200, y + 78)
            d.text((x + 210, y + 12), "-3.7%", font=font(SANS_B, 22),
                   fill=RED)
            d.text((x + 210, y + 42), "S&P 500", font=font(SANS, 13),
                   fill=(90, 90, 90))
        elif kind == "quake":
            draw_quake(d, x + 8, y + 6, x + 210, y + 78)
            d.text((x + 216, y + 12), "6.9", font=font(SANS_B, 26), fill=INK)
            d.text((x + 216, y + 42), "magnitude", font=font(SANS, 12),
                   fill=(90, 90, 90))
        elif kind == "space":
            d.rectangle([x, y + 4, x + 220, y + 88], fill=(10, 16, 32))
            draw_space(d, x + 110, y + 46)
        y2 = headline(d, x, y + 92, w, head, size=18)
        caption(d, x, y2 + 2, w, cap, size=12)

    # numbers panel (bottom right)
    x0, y0 = cols[2], rows[1]
    x, y, w = panel(d, (x0, y0, x0 + cw, y0 + ch), "THE DAY IN NUMBERS",
                    INK)
    stats = [("200", "countries at COP31"),
             ("60", "wounded in Kryvyi Rih"),
             ("8 yrs", "BepiColombo's trip"),
             ("-5.1%", "Nikkei's Friday fall")]
    yy = y + 2
    for num, label in stats:
        d.text((x, yy), num, font=font(SANS_B, 20), fill=RED)
        d.text((x + 92, yy + 4), label, font=font(SANS, 14), fill=INK)
        yy += 32

    # ---- footer ----
    d.line([24, 792, 1000, 792], fill=RULE, width=2)
    d.text((24, 797), "Compiled from AP, Reuters, NYT, ESA and USGS reports "
           "of 21 November 2026.", font=font(SANS, 11), fill=(90, 90, 90))
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
