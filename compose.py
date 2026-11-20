"""Compose the news-image-20261120 front page.

Masthead + lead band (Trump-Xi-Putin peace declaration, Shenzhen) +
five illustrated headline rows + ticker. Everything is drawn with PIL
(no generated media, no network). Writes a 1024x1024 JPEG (<=1 MiB)
to news.jpg next to this file. Deterministic: no timestamps, no
randomness in the image bytes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news.jpg")

W, H = 1024, 1024

# palette
INK_NAVY = (12, 26, 44)
BAND = (23, 41, 66)
BAND_DARK = (18, 33, 54)
GOLD = (212, 175, 105)
PAPER = (247, 243, 234)
PAPER_ALT = (255, 255, 255)
BLACK = (22, 22, 22)
SUBGREY = (64, 64, 64)
MUTED = (96, 96, 96)
PALE = (205, 212, 220)
RULE = (220, 214, 200)
CRIMSON = (178, 34, 34)
STEEL = (26, 82, 118)
VIOLET = (125, 60, 152)
GREEN = (17, 120, 100)
OCHRE = (176, 106, 12)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_title = ImageFont.truetype(SERIF_BOLD, 48)
f_dateline = ImageFont.truetype(SANS_BOLD, 21)
f_kicker = ImageFont.truetype(SANS_BOLD, 18)
f_lead1 = ImageFont.truetype(SANS_BOLD, 36)
f_lead2 = ImageFont.truetype(SANS, 20)
f_headline = ImageFont.truetype(SANS_BOLD, 27)
f_summary = ImageFont.truetype(SANS, 20)
f_ticker_b = ImageFont.truetype(SANS_BOLD, 17)
f_ticker = ImageFont.truetype(SANS, 17)
f_badge = ImageFont.truetype(SANS_BOLD, 15)
f_caption = ImageFont.truetype(SANS, 14)


def greedy_wrap(draw, text, font, max_width):
    """Greedy word wrap returning lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_to_lines(draw, text, font, max_width, max_lines):
    """Wrap text, trimming from the end with an ellipsis if it overflows."""
    lines = greedy_wrap(draw, text, font, max_width)
    while len(lines) > max_lines and len(text) > 12:
        text = text[:-1].rstrip()
        if text.endswith(","):
            text = text[:-1]
        lines = greedy_wrap(draw, text + " ...", font, max_width)
    return lines


page = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(page)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 96], fill=INK_NAVY)
d.text((W // 2, 8), "THE WORLD", font=f_title, fill=(255, 255, 255),
       anchor="ma")
d.text((W // 2, 66), "FRIDAY  \u00b7  20 NOVEMBER 2026", font=f_dateline,
       fill=GOLD, anchor="ma")
d.rectangle([0, 96, W, 100], fill=GOLD)

# ------------------------------------------------------------- lead band
BAND_TOP, BAND_BOT = 100, 308
d.rectangle([0, BAND_TOP, W, BAND_BOT], fill=BAND)
# low skyline silhouette along the band's bottom edge
for sx, sw, sh in ((330, 60, 26), (400, 44, 40), (452, 70, 22),
                   (530, 52, 34), (590, 90, 20), (690, 48, 38),
                   (746, 66, 24), (820, 56, 32), (884, 80, 18),
                   (972, 40, 28)):
    d.rectangle([sx, BAND_BOT - sh, sx + sw, BAND_BOT], fill=BAND_DARK)

# --- left panel: three flags, three leaders, declaration seal ---
PX, PY = 30, 116
for pole_x in (PX + 28, PX + 118, PX + 208):
    d.line([(pole_x, PY - 4), (pole_x, PY + 44)], fill=GOLD, width=3)
    d.ellipse([pole_x - 4, PY - 9, pole_x + 4, PY - 1], fill=GOLD)


def draw_flag_usa(x, y, w=62, h=34):
    for stripe in range(7):
        d.rectangle([x, y + stripe * h // 7, x + w,
                     y + (stripe + 1) * h // 7],
                    fill=CRIMSON if stripe % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(26, 42, 108))
    for row in range(2):
        for col in range(3):
            sx, sy = x + 6 + col * 9, y + 5 + row * 8
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))


def draw_flag_china(x, y, w=62, h=34):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + 6, y + 5, x + 16, y + 15], fill=(255, 222, 0))
    for sx, sy in ((x + 22, y + 4), (x + 28, y + 10), (x + 28, y + 18),
                   (x + 22, y + 24)):
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 222, 0))


def draw_flag_russia(x, y, w=62, h=34):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


draw_flag_usa(PX, PY + 2)
draw_flag_china(PX + 90, PY + 2)
draw_flag_russia(PX + 180, PY + 2)
d.text((PX + 121, PY + 48), "USA  \u00b7  CHINA  \u00b7  RUSSIA",
       font=f_badge, fill=PALE, anchor="ma")

# three leader busts, one under each flag
SKIN = (232, 190, 150)
for centre_x, tie_colour in ((PX + 31, CRIMSON), (PX + 121, (255, 222, 0)),
                             (PX + 211, (0, 57, 166))):
    d.rounded_rectangle([centre_x - 32, PY + 100, centre_x + 32, PY + 150],
                        radius=12, fill=(74, 96, 128))
    d.polygon([(centre_x - 10, PY + 102), (centre_x + 10, PY + 102),
               (centre_x, PY + 122)], fill=(255, 255, 255))
    d.polygon([(centre_x - 6, PY + 104), (centre_x + 6, PY + 104),
               (centre_x, PY + 132)], fill=tie_colour)
    d.ellipse([centre_x - 15, PY + 72, centre_x + 15, PY + 102], fill=SKIN)
d.text((PX + 121, PY + 158), "SHENZHEN", font=f_badge, fill=GOLD,
       anchor="ma")

# --- lead text, right of the illustration ---
LX = 356
d.text((LX, 118), "APEC SUMMIT  \u00b7  THE LEAD", font=f_kicker, fill=GOLD)
d.text((LX, 146), "TRUMP, XI, PUTIN SIGN", font=f_lead1, fill=(255, 255, 255))
d.text((LX, 188), "\u2018PEACE DECLARATION\u2019", font=f_lead1,
       fill=(255, 255, 255))
lead_body = ("First-ever trilateral: \u201ca nuclear war cannot be won and "
             "must never be fought\u201d \u2014 but no word on Ukraine or "
             "Iran.")
for i, line in enumerate(greedy_wrap(d, lead_body, f_lead2, W - LX - 28)):
    d.text((LX, 236 + i * 26), line, font=f_lead2, fill=PALE)
d.rectangle([0, BAND_BOT, W, BAND_BOT + 3], fill=GOLD)

# ------------------------------------------------------------ story rows
def pic_clock(dd, x0, y0):
    # calendar page with a clock face: the Iran decision pushed to 2027
    dd.rounded_rectangle([x0 + 8, y0 + 10, x0 + 56, y0 + 56], radius=6,
                         outline=(255, 255, 255), width=3)
    dd.line([(x0 + 8, y0 + 22), (x0 + 56, y0 + 22)], fill=(255, 255, 255),
            width=3)
    dd.line([(x0 + 20, y0 + 6), (x0 + 20, y0 + 14)], fill=(255, 255, 255),
            width=3)
    dd.line([(x0 + 44, y0 + 6), (x0 + 44, y0 + 14)], fill=(255, 255, 255),
            width=3)
    dd.ellipse([x0 + 20, y0 + 28, x0 + 44, y0 + 52],
               outline=(255, 255, 255), width=3)
    dd.line([(x0 + 32, y0 + 40), (x0 + 32, y0 + 33)], fill=(255, 255, 255),
            width=2)
    dd.line([(x0 + 32, y0 + 40), (x0 + 39, y0 + 40)], fill=(255, 255, 255),
            width=2)


def pic_scales(dd, x0, y0):
    # scales of justice
    dd.line([(x0 + 32, y0 + 8), (x0 + 32, y0 + 54)], fill=(255, 255, 255),
            width=3)
    dd.line([(x0 + 10, y0 + 14), (x0 + 54, y0 + 14)], fill=(255, 255, 255),
            width=3)
    dd.ellipse([x0 + 28, y0 + 4, x0 + 36, y0 + 12], fill=(255, 255, 255))
    for cx in (14, 50):
        dd.line([(x0 + cx, y0 + 14), (x0 + cx - 8, y0 + 34)],
                fill=(255, 255, 255), width=2)
        dd.line([(x0 + cx, y0 + 14), (x0 + cx + 8, y0 + 34)],
                fill=(255, 255, 255), width=2)
        dd.arc([x0 + cx - 10, y0 + 30, x0 + cx + 10, y0 + 44], 0, 180,
               fill=(255, 255, 255), width=3)
    dd.rectangle([x0 + 20, y0 + 54, x0 + 44, y0 + 58], fill=(255, 255, 255))


def pic_controller(dd, x0, y0):
    # neon skyline behind a game controller
    for bx, bw, bh in ((4, 10, 18), (18, 8, 26), (30, 12, 14), (46, 8, 22)):
        dd.rectangle([x0 + bx, y0 + 58 - bh, x0 + bx + bw, y0 + 58],
                     fill=(200, 170, 255))
    dd.rounded_rectangle([x0 + 8, y0 + 14, x0 + 56, y0 + 50], radius=10,
                         outline=(255, 255, 255), width=3)
    dd.line([(x0 + 18, y0 + 26), (x0 + 26, y0 + 26)], fill=(255, 255, 255),
            width=3)
    dd.line([(x0 + 22, y0 + 22), (x0 + 22, y0 + 30)], fill=(255, 255, 255),
            width=3)
    dd.ellipse([x0 + 38, y0 + 24, x0 + 44, y0 + 30], fill=(255, 255, 255))
    dd.ellipse([x0 + 44, y0 + 30, x0 + 50, y0 + 36], fill=(255, 255, 255))


def pic_cyclone(dd, x0, y0):
    # spiral storm over a coastline
    for radius in (24, 18, 12, 6):
        dd.arc([x0 + 32 - radius, y0 + 30 - radius, x0 + 32 + radius,
                y0 + 30 + radius], 200, 200 + 270,
               fill=(255, 255, 255), width=3)
    dd.ellipse([x0 + 28, y0 + 26, x0 + 36, y0 + 34], fill=(255, 200, 90))
    for wx in (6, 22, 38, 54):
        dd.line([(x0 + wx, y0 + 56), (x0 + wx + 4, y0 + 52)],
                fill=(255, 255, 255), width=2)


def pic_tower(dd, x0, y0):
    # skyscraper with a blast star and broken windows
    dd.rectangle([x0 + 22, y0 + 6, x0 + 42, y0 + 58], fill=(255, 255, 255))
    dd.rectangle([x0 + 14, y0 + 22, x0 + 22, y0 + 58], fill=(200, 210, 220))
    dd.rectangle([x0 + 42, y0 + 22, x0 + 50, y0 + 58], fill=(200, 210, 220))
    for wy in (14, 24, 34):
        dd.rectangle([x0 + 26, y0 + wy, x0 + 30, y0 + wy + 4],
                     fill=(255, 200, 90))
        dd.rectangle([x0 + 34, y0 + wy, x0 + 38, y0 + wy + 4],
                     fill=(255, 200, 90))
    for angle in range(8):
        a = angle * math.pi / 4
        dd.line([(x0 + 52 + 5 * math.cos(a), y0 + 14 + 5 * math.sin(a)),
                 (x0 + 52 + 11 * math.cos(a), y0 + 14 + 11 * math.sin(a))],
                fill=(255, 200, 90), width=2)


STORIES = [
    (CRIMSON, pic_clock, "1",
     "TRUMP PUSHES IRAN CALL TO 2027",
     "\u201cNo rush,\u201d he says \u2014 the war decision comes \u201cafter "
     "Jan 1\u201d; hawks told to wait."),
    (GREEN, pic_scales, "2",
     "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
     "First state ever found guilty; about 10,000 Rohingya killed in "
     "2017; reparations ordered."),
    (VIOLET, pic_controller, "3",
     "GTA VI: $1.84 BILLION IN A DAY",
     "19 million copies in 24 hours; 99 on Metacritic \u2014 the "
     "best-reviewed game ever."),
    (STEEL, pic_cyclone, "4",
     "CYCLONE AKVAN: 300,000 EVACUATED",
     "Storm bears down on India\u2019s Odisha coast; schools shut and "
     "rescue teams deployed."),
    (OCHRE, pic_tower, "5",
     "HOUTHI MISSILE HITS RIYADH TOWER",
     "Saudi wealth fund HQ damaged across 7\u20138 floors; no injuries; "
     "second strike in two weeks."),
]

ROWS_TOP, ROW_HEIGHT = 311, 117
for index, (colour, picture, number, headline, summary) in enumerate(STORIES):
    y0 = ROWS_TOP + index * ROW_HEIGHT
    d.rectangle([0, y0, W, y0 + ROW_HEIGHT],
                fill=PAPER_ALT if index % 2 == 1 else PAPER)
    d.line([(0, y0 + ROW_HEIGHT - 1), (W, y0 + ROW_HEIGHT - 1)], fill=RULE,
           width=1)
    # icon chip
    chip_x, chip_y = 28, y0 + 14
    d.rounded_rectangle([chip_x, chip_y, chip_x + 88, chip_y + 88],
                        radius=12, fill=colour)
    picture(d, chip_x + 12, chip_y + 12)
    d.ellipse([chip_x + 66, chip_y - 4, chip_x + 92, chip_y + 22],
              fill=GOLD, outline=(255, 255, 255), width=2)
    d.text((chip_x + 79, chip_y + 8), number, font=f_badge, fill=INK_NAVY,
           anchor="mm")
    text_x = 140
    headline_lines = fit_to_lines(d, headline, f_headline, W - text_x - 28, 1)
    d.text((text_x, y0 + 16), headline_lines[0], font=f_headline, fill=BLACK)
    summary_lines = fit_to_lines(d, summary, f_summary, W - text_x - 28, 2)
    for j, line in enumerate(summary_lines):
        d.text((text_x, y0 + 52 + j * 26), line, font=f_summary,
               fill=SUBGREY)

# ------------------------------------------------------------------ ticker
TICK_TOP = ROWS_TOP + 5 * ROW_HEIGHT + 4  # 900
d.rectangle([0, TICK_TOP, W, TICK_TOP + 64], fill=INK_NAVY)
d.text((28, TICK_TOP + 20), "ALSO TODAY", font=f_ticker_b, fill=GOLD)
ticker = ("Voyager 1 passes one light-day from Earth  \u00b7  Anthropic "
          "debuts among the world\u2019s most valuable companies  "
          "\u00b7  Crimean Bridge hit a third time  \u00b7  Van Gogh sells "
          "for a record $190.4m")
ticker_lines = greedy_wrap(d, ticker, f_ticker, W - 190)
for j, line in enumerate(ticker_lines[:2]):
    d.text((186, TICK_TOP + 8 + j * 26), line, font=f_ticker, fill=(255, 255, 255))
d.rectangle([0, TICK_TOP + 64, W, TICK_TOP + 68], fill=GOLD)

# ------------------------------------------------------------------ footer
d.text((W // 2, TICK_TOP + 80),
       "Compiled early 20 Nov 2026 (~01:30 UTC) \u2014 the day continues  "
       "\u00b7  Sources: Reuters, BBC, AP, CNN, USA Today, UN",
       font=f_caption, fill=MUTED, anchor="ma")

page.save(OUT, "JPEG", quality=88, optimize=True)
print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")
