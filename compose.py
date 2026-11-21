# compose.py — draws news.jpg for news-image-20261120 (round 3, full-day edition).
# Front page for Friday 20 November 2026, compiled AFTER the day ended.
# All stories verified against Reuters / BBC / CNN / AP / ISW / UN reporting
# for 20 Nov 2026. Pure PIL drawing, no photographs, no network.
# Run: python3 compose.py  ->  writes news.jpg (1024x1024) next to this file.

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (13, 27, 62)
NAVY2 = (24, 44, 84)
NAVY_DARK = (7, 14, 34)
GOLD = (201, 162, 75)
GOLD_LT = (233, 197, 110)
CREAM = (247, 243, 234)
WHITE = (255, 255, 255)
INK = (18, 22, 32)
GREY = (88, 94, 108)
LINE = (216, 210, 196)
FIRE = (255, 122, 26)
EMBER = (255, 190, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, s, path, start, max_w, floor=30):
    size = start
    while size > floor and text_w(draw, s, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def star(draw, cx, cy, r, color, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(1, 7, 2):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=WHITE)
    cw, ch = w * 0.42, h * 4 / 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(28, 48, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * cw / 4.4, y + 3 + r * ch / 3.4,
                          x + 8 + c * cw / 4.4, y + 7 + r * ch / 3.4], fill=WHITE)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.20, y + h * 0.28, h * 0.20, (255, 222, 0))
    for sx, sy in [(0.52, 0.14), (0.66, 0.26), (0.66, 0.48), (0.52, 0.60)]:
        star(draw, x + w * sx, y + h * sy, h * 0.08, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 90, 180))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(220, 30, 30))


def bust(draw, cx, base_y, r, skin, suit, tie):
    draw.ellipse([cx - r, base_y - 2 * r - 14, cx + r, base_y - 14], fill=skin)
    draw.pieslice([cx - r - 8, base_y - 26, cx + r + 8, base_y + 26], 180, 360, fill=suit)
    draw.polygon([(cx - 5, base_y - 24), (cx + 5, base_y - 24),
                  (cx + 9, base_y - 4), (cx, base_y + 2), (cx - 9, base_y - 4)], fill=tie)
    draw.polygon([(cx - 12, base_y - 26), (cx, base_y - 14), (cx + 12, base_y - 26)],
                 fill=(235, 235, 235))


def icon_scales(d, x, y, s, col):
    d.line([(x + s / 2, y + 6), (x + s / 2, y + s - 12)], fill=col, width=4)
    d.line([(x + 8, y + 16), (x + s - 8, y + 16)], fill=col, width=4)
    d.ellipse([x + s / 2 - 4, y + 4, x + s / 2 + 4, y + 12], fill=col)
    for sx in (x + 8, x + s - 8):
        d.line([(sx, y + 16), (sx - 9, y + s - 22)], fill=col, width=3)
        d.line([(sx, y + 16), (sx + 9, y + s - 22)], fill=col, width=3)
        d.arc([sx - 11, y + s - 26, sx + 11, y + s - 8], 0, 180, fill=col, width=3)
    d.line([(x + s / 2 - 12, y + s - 8), (x + s / 2 + 12, y + s - 8)], fill=col, width=4)


def icon_calendar(d, x, y, s, col):
    d.rounded_rectangle([x + 6, y + 10, x + s - 6, y + s - 6], 6, outline=col, width=4)
    d.line([(x + 6, y + 22), (x + s - 6, y + 22)], fill=col, width=4)
    d.line([(x + 18, y + 4), (x + 18, y + 14)], fill=col, width=4)
    d.line([(x + s - 18, y + 4), (x + s - 18, y + 14)], fill=col, width=4)
    d.ellipse([x + s / 2 - 13, y + 30, x + s / 2 + 13, y + s - 12], outline=col, width=4)
    d.line([(x + s / 2, y + s / 2 - 2), (x + s / 2, y + 36)], fill=col, width=3)
    d.line([(x + s / 2, y + s / 2 - 2), (x + s / 2 + 8, y + s / 2 + 5)], fill=col, width=3)


def icon_chart_down(d, x, y, s, col):
    d.line([(x + 8, y + 8), (x + 8, y + s - 8), (x + s - 6, y + s - 8)], fill=col, width=4)
    pts = [(x + 12, y + 16), (x + 24, y + 26), (x + 34, y + 20),
           (x + 46, y + 34), (x + s - 10, y + s - 16)]
    d.line(pts, fill=col, width=5, joint="curve")
    ex, ey = x + s - 10, y + s - 16
    d.polygon([(ex, ey), (ex - 12, ey - 1), (ex - 2, ey - 12)], fill=col)


def icon_gamepad(d, x, y, s, col):
    d.rounded_rectangle([x + 4, y + 16, x + s - 4, y + s - 14], 12, outline=col, width=4)
    d.line([(x + 16, y + s / 2 + 2), (x + 28, y + s / 2 + 2)], fill=col, width=5)
    d.line([(x + 22, y + s / 2 - 4), (x + 22, y + s / 2 + 8)], fill=col, width=5)
    d.ellipse([x + s - 26, y + s / 2 - 8, x + s - 18, y + s / 2], fill=col)
    d.ellipse([x + s - 26, y + s / 2 + 4, x + s - 18, y + s / 2 + 12], fill=col)
    d.line([(x + 10, y + 22), (x + s - 10, y + 22)], fill=col, width=3)


def icon_cyclone(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    for i, r in enumerate((24, 18, 12, 6)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200 - i * 40, 200 - i * 40 + 250,
              fill=col, width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)
    for ang in (30, 150, 270):
        a = math.radians(ang)
        d.line([(cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
                (cx + 33 * math.cos(a), cy + 33 * math.sin(a))], fill=col, width=3)


ICONS = {"scales": icon_scales, "calendar": icon_calendar,
         "chartdown": icon_chart_down, "gamepad": icon_gamepad,
         "cyclone": icon_cyclone}

ROWS = [
    ("WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
     "First state ever convicted of genocide; about 10,000 Rohingya killed "
     "in 2017; reparations ordered.",
     (14, 120, 88), "scales"),
    ("TRUMP: NO IRAN DECISION UNTIL 2027",
     "\u201cNo rush,\u201d he says \u2014 the call comes \u201cafter Jan 1\u201d; "
     "Vance won\u2019t say he\u2019d have ordered strikes.",
     (178, 44, 44), "calendar"),
    ("MARKETS SLIDE AS ANTHROPIC FALLS",
     "A day after its $2 trillion debut \u2014 up 17% to $97 \u2014 Anthropic "
     "slides; tech sell-off pushes the S&P 500 and Dow into correction.",
     (64, 56, 120), "chartdown"),
    ("GTA VI: $3.79 BILLION IN A DAY",
     "Take-Two confirms 32.5 million copies in 24 hours \u2014 the biggest "
     "entertainment launch ever.",
     (122, 63, 160), "gamepad"),
    ("CYCLONE AKVAN HITS INDIA\u2019S COAST",
     "Storm makes landfall near Gopalpur, Odisha; 300,000 evacuated; "
     "schools shut and rescue teams deployed.",
     (14, 110, 130), "cyclone"),
]

TICKER = ("UK\u2013EU strike a new deal \u00b7 Houthi missile hits a Riyadh tower "
          "\u00b7 Kenya\u2019s last Ebola patient home \u00b7 COP31 talks run into "
          "overtime \u00b7 Voyager 1 passes one light-day out")


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    rnd = random.Random(20261120)

    # ---- masthead ----
    d.rectangle([0, 0, W, 92], fill=NAVY)
    f_title = font(SERIF_B, 62)
    t = "THE WORLD"
    d.text(((W - text_w(d, t, f_title)) / 2, 6), t, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 23)
    dt = "FRIDAY  \u00b7  20 NOVEMBER 2026"
    d.text(((W - text_w(d, dt, f_date)) / 2, 66), dt, font=f_date, fill=GOLD_LT)
    d.rectangle([0, 92, W, 96], fill=GOLD)

    # ---- lead block ----
    LY = 96
    d.rectangle([0, LY, W, LY + 350], fill=NAVY2)
    f_kick = font(SANS_B, 19)
    kick = "SHENZHEN \u00b7 THE TRILATERAL \u2014 AND WHAT FOLLOWED"
    d.text((20, LY + 12), kick, font=f_kick, fill=GOLD_LT)
    head = "PEACE DECLARED. THEN 110 MISSILES."
    f_head = fit_font(d, head, SANS_B, 54, W - 40)
    d.text((20, LY + 38), head, font=f_head, fill=WHITE)

    # two scene panels
    py, ph = LY + 108, 148
    pw = (W - 56) // 2
    lx, rx = 20, 20 + pw + 16

    # left: the signing, Shenzhen (daylight)
    vgrad(d, (lx, py, lx + pw, py + ph), (242, 212, 146), (214, 164, 92))
    d.rectangle([lx, py + ph - 46, lx + pw, py + ph], fill=(122, 84, 48))
    # table + document
    d.rectangle([lx + 150, py + ph - 78, lx + pw - 150, py + ph - 40], fill=(96, 62, 34))
    d.rectangle([lx + pw // 2 - 62, py + ph - 74, lx + pw // 2 + 62, py + ph - 44],
                fill=(252, 250, 244))
    for i in range(3):
        d.line([(lx + pw // 2 - 50, py + ph - 66 + i * 8),
                (lx + pw // 2 + 50, py + ph - 66 + i * 8)], fill=(150, 150, 150), width=2)
    d.ellipse([lx + pw // 2 + 34, py + ph - 58, lx + pw // 2 + 50, py + ph - 42],
              fill=(178, 34, 52))
    # three flags on poles
    fw, fh = 74, 44
    for i, fn in enumerate((flag_us, flag_cn, flag_ru)):
        fx = lx + 42 + i * (pw - 84 - fw) // 2
        d.line([(fx + fw // 2, py + 8), (fx + fw // 2, py + 8 + fh + 12)],
               fill=(90, 60, 30), width=3)
        fn(d, fx, py + 10, fw, fh)
    # three busts behind the table
    for i, (skin, suit, tie) in enumerate((
            ((232, 190, 150), (40, 48, 66), (178, 34, 52)),
            ((238, 205, 170), (52, 52, 52), (222, 180, 0)),
            ((226, 182, 140), (36, 44, 60), (0, 90, 180)))):
        cx = lx + 90 + i * (pw - 180) // 2
        bust(d, cx, py + ph - 46, 20, skin, suit, tie)
    d.rectangle([lx, py + ph - 24, lx + pw, py + ph], fill=NAVY_DARK)
    f_cap = font(SANS_B, 15)
    d.text((lx + 10, py + ph - 21), "THE SIGNING \u00b7 SHENZHEN", font=f_cap, fill=WHITE)

    # right: hours later, Kyiv (night)
    vgrad(d, (rx, py, rx + pw, py + ph), (16, 26, 54), (4, 8, 20))
    for _ in range(26):
        sx, sy = rx + rnd.randint(4, pw - 4), py + rnd.randint(4, ph - 60)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 235))
    # river
    d.rectangle([rx, py + ph - 40, rx + pw, py + ph], fill=(10, 22, 46))
    for i in range(5):
        x0 = rx + 30 + i * 90
        d.line([(x0, py + ph - 26), (x0 + 44, py + ph - 26)], fill=(70, 110, 170), width=2)
    # bridge silhouette
    bx0, bx1 = rx + 24, rx + pw - 24
    by = py + ph - 40
    d.rectangle([bx0, by - 10, bx1, by], fill=(46, 60, 92))
    for i in range(4):
        px = bx0 + 18 + i * (bx1 - bx0 - 36) // 3
        d.rectangle([px, by - 34, px + 7, by - 10], fill=(46, 60, 92))
        d.line([(px + 3, by - 34), (px + 3, by - 58)], fill=(46, 60, 92), width=3)
    d.line([(bx0 + 10, by - 12), (bx1 - 10, by - 12)], fill=(150, 160, 190), width=2)
    for i in range(9):
        lx2 = bx0 + 16 + i * (bx1 - bx0 - 32) // 8
        d.ellipse([lx2, by - 16, lx2 + 3, by - 13], fill=(255, 214, 120))
    # missile streaks
    for (mx, my, ln) in ((rx + 60, py + 18, 74), (rx + 250, py + 8, 88), (rx + 380, py + 30, 60)):
        d.line([(mx, my), (mx + ln, my + ln // 2)], fill=(255, 220, 130), width=4)
        d.ellipse([mx + ln - 4, my + ln // 2 - 4, mx + ln + 6, my + ln // 2 + 6],
                  fill=(255, 240, 200))
    # explosion glow over the bridge (soft, many small alpha steps)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ex, ey = rx + pw // 2 - 30, by - 30
    for r, a in ((48, 18), (42, 26), (36, 36), (30, 50), (24, 68),
                 (18, 92), (12, 130), (7, 200)):
        gd.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 122, 26, a))
    gd.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 230, 150, 255))
    for (sx, sy) in ((ex - 26, ey - 22), (ex + 24, ey - 30), (ex + 34, ey - 8)):
        gd.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 200, 90, 220))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([rx, py + ph - 24, rx + pw, py + ph], fill=NAVY_DARK)
    d.text((rx + 10, py + ph - 21), "HOURS LATER \u00b7 KYIV", font=f_cap, fill=WHITE)

    # lead sub
    f_sub = font(SANS, 20)
    sub = ("Hours after Trump, Xi and Putin issued a \u2018peace declaration\u2019 in "
           "Shenzhen, Russia fired 110+ missiles and 400 drones at Ukraine \u2014 "
           "three Kyiv bridges hit, 8 killed, and missiles crashed into Poland.")
    lines = wrap(d, sub, f_sub, W - 40)
    y = LY + 108 + ph + 10
    for ln in lines:
        d.text((20, y), ln, font=f_sub, fill=(226, 232, 242))
        y += 22

    # ---- story rows ----
    ry = LY + 350
    rh = 92
    f_h = font(SANS_B, 29)
    f_s = font(SANS, 20)
    for i, (headline, sub, tile, icon) in enumerate(ROWS):
        y0 = ry + i * rh
        if i % 2 == 1:
            d.rectangle([0, y0, W, y0 + rh], fill=CREAM)
        # icon tile + number badge
        tx, ty = 20, y0 + (rh - 76) // 2
        d.rounded_rectangle([tx, ty, tx + 76, ty + 76], 14, fill=tile)
        ICONS[icon](d, tx + 12, ty + 12, 52, WHITE)
        d.ellipse([tx + 54, ty - 6, tx + 82, ty + 22], fill=GOLD, outline=WHITE, width=2)
        f_n = font(SANS_B, 17)
        num = str(i + 1)
        d.text((tx + 68 - text_w(d, num, f_n) / 2, ty - 3), num, font=f_n, fill=NAVY_DARK)
        # headline + sub
        hx = 124
        d.text((hx, y0 + 10), headline, font=f_h, fill=INK)
        slines = wrap(d, sub, f_s, W - hx - 20)
        sy = y0 + 48
        for ln in slines[:2]:
            d.text((hx, sy), ln, font=f_s, fill=(52, 58, 70))
            sy += 23
        if i < 4:
            d.line([(0, y0 + rh), (W, y0 + rh)], fill=LINE, width=1)

    # ---- ticker ----
    ty0 = ry + 5 * rh
    d.rectangle([0, ty0, W, ty0 + 68], fill=NAVY)
    f_lab = font(SANS_B, 18)
    d.text((20, ty0 + 24), "ALSO TODAY", font=f_lab, fill=GOLD_LT)
    f_t = font(SANS, 18)
    tlines = wrap(d, TICKER, f_t, W - 190)
    yy = ty0 + 7
    for ln in tlines[:3]:
        d.text((176, yy), ln, font=f_t, fill=WHITE)
        yy += 22

    # ---- footer ----
    fy0 = ty0 + 68
    f_f = font(SANS, 16)
    f1 = ("Compiled after the day ended \u2014 the full Friday, 20 November 2026 "
          "\u00b7 every story first reported that day.")
    f2 = "Sources: Reuters \u00b7 BBC \u00b7 CNN \u00b7 AP \u00b7 ISW \u00b7 UN  \u2014  Drawn with code; no photographs."
    d.text(((W - text_w(d, f1, f_f)) / 2, fy0 + 8), f1, font=f_f, fill=GREY)
    d.text(((W - text_w(d, f2, f_f)) / 2, fy0 + 30), f2, font=f_f, fill=GREY)

    img.save("news.jpg", quality=88)
    print("wrote news.jpg", img.size)


if __name__ == "__main__":
    main()
