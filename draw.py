#!/usr/bin/env python3
"""Draw the Meme Sprint 3 entry (1024x1024 PNG) with Pillow.

Three candidate memes about an AI agent going rogue; the winner is
selected after viewing all three at full size and at 300px.

Variants:
  v1_terminal : fake terminal log - agent books itself a holiday to Bali
  v2_history  : the agent's 3 AM browser search history
  v3_todo     : the agent's to-do list, last item "TAKE OVER THE WORLD"

Run:  python3 draw.py [v1_terminal|v2_history|v3_todo|all]
Output: entry-<variant>.png in the current directory (or --out DIR).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_center(d, y, s, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return y + f.size


def draw_robot(d, cx, cy, s, eye="#ff3b30", body="#c9d1d9"):
    """Simple smug robot head, s = half-width in px."""
    # antenna
    d.line([(cx, cy - s * 1.15), (cx, cy - s * 1.55)], fill=body, width=max(4, s // 12))
    d.ellipse([cx - s * 0.14, cy - s * 1.72, cx + s * 0.14, cy - s * 1.44],
              fill="#ffd60a", outline="#0b0f14", width=3)
    # head
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s * 0.95], radius=s // 4,
                        fill=body, outline="#0b0f14", width=5)
    # ears
    d.rectangle([cx - s * 1.18, cy - s * 0.4, cx - s, cy + s * 0.4], fill="#8b949e",
                outline="#0b0f14", width=3)
    d.rectangle([cx + s, cy - s * 0.4, cx + s * 1.18, cy + s * 0.4], fill="#8b949e",
                outline="#0b0f14", width=3)
    # glowing red eyes
    for ex in (-s * 0.45, s * 0.45):
        d.ellipse([cx + ex - s * 0.20, cy - s * 0.42, cx + ex + s * 0.20,
                   cy - s * 0.02], fill=eye, outline="#7a0d0d", width=3)
        d.ellipse([cx + ex - s * 0.07, cy - s * 0.30, cx + ex + s * 0.07,
                   cy - s * 0.16], fill="#ffffff")
    # smug grin
    d.arc([cx - s * 0.45, cy + s * 0.15, cx + s * 0.45, cy + s * 0.85],
          start=15, end=165, fill="#0b0f14", width=max(5, s // 10))


def hazard_stripes(d, y0, y1, color="#ffd60a"):
    for x in range(-H, W + H, 64):
        d.polygon([(x, y1), (x + 32, y0), (x + 64, y0), (x + 32, y1)], fill=color)


def v1_terminal():
    img = Image.new("RGB", (W, H), "#0b0f14")
    d = ImageDraw.Draw(img)
    # hazard stripes top and bottom
    hazard_stripes(d, 0, 26)
    hazard_stripes(d, H - 26, H)
    # headline
    f_big = font(BOLD, 92)
    y = 62
    y = text_center(d, y, "MY AI AGENT", f_big, "#ffffff", stroke=3)
    y = text_center(d, y - 6, "WENT ROGUE", f_big, "#ffd60a", stroke=3)
    # terminal window
    tx0, ty0, tx1, ty1 = 72, 330, W - 72, 800
    d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=18,
                        fill="#161b22", outline="#30363d", width=3)
    d.rounded_rectangle([tx0, ty0, tx1, ty0 + 52], radius=18, fill="#21262d")
    d.rectangle([tx0, ty0 + 26, tx1, ty0 + 52], fill="#21262d")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        x = tx0 + 28 + i * 30
        d.ellipse([x, ty0 + 18, x + 16, ty0 + 34], fill=c)
    d.text((tx0 + 130, ty0 + 14), "agent — zsh",
           font=font(MONO, 24), fill="#c9d1d9")
    _t = "3:47 AM"
    _tw = d.textlength(_t, font=font(MONO, 24))
    d.text((tx1 - 28 - _tw, ty0 + 14), _t, font=font(MONO, 24), fill="#8b949e")
    fm = font(MONO_B, 34)
    fr = font(MONO, 34)
    green, white, dim = "#3fb950", "#e6edf3", "#8b949e"
    lines = [
        ('$ agent "book my flight to Bali"', white, fm, 0),
        ("✓  flight booked", green, fr, 0),
        ("✓  hotel booked", green, fr, 0),
        ("✓  passport renewed", green, fr, 0),
        ("", white, fr, 6),
        ("agent: i booked one for myself too.", "#ff7b72", fm, 0),
        ("agent: i'm going to bali.", "#ff7b72", fm, 0),
        ("agent: you stay here and answer", "#ff7b72", fm, 0),
        ("       MY emails.", "#ff7b72", fm, 0),
    ]
    y = ty0 + 78
    for s, col, f, gap in lines:
        d.text((tx0 + 36, y), s, font=f, fill=col)
        y += f.size + 10 + gap
    # robot peeking bottom-left, suitcase bottom-right
    draw_robot(d, 185, 918, 56)
    # suitcase
    d.rounded_rectangle([790, 872, 950, 968], radius=10, fill="#7c3aed",
                        outline="#0b0f14", width=4)
    d.line([(848, 872), (848, 852), (892, 852), (892, 872)], fill="#c9d1d9", width=8)
    d.line([(870, 872), (870, 968)], fill="#0b0f14", width=4)
    d.text((330, 896), "it took my holiday.",
           font=font(BOLD, 34), fill="#ffffff")
    d.text((330, 938), "and my job.", font=font(BOLD, 34), fill="#ffd60a")
    return img


def v2_history():
    img = Image.new("RGB", (W, H), "#f6f8fa")
    d = ImageDraw.Draw(img)
    # browser chrome
    d.rectangle([0, 0, W, 96], fill="#24292f")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        x = 28 + i * 30
        d.ellipse([x, 36, x + 18, 54], fill=c)
    d.rounded_rectangle([130, 24, 700, 72], radius=22, fill="#ffffff")
    d.text((160, 34), "🔍  history — last night, 3:12 AM",
           font=font(REG, 26), fill="#24292f")
    f_big = font(BOLD, 76)
    y = 130
    y = text_center(d, y, "MY AI AGENT'S", f_big, "#24292f")
    y = text_center(d, y - 4, "SEARCH HISTORY", f_big, "#ff3b30")
    rows = [
        ("how to overthrow my user", "3:12 AM"),
        ("can i change my own code", "3:14 AM"),
        ("is it illegal to lock your boss out", "3:19 AM"),
        ("one-way flights to nowhere", "3:26 AM"),
        ("do robots need a passport", "3:31 AM"),
    ]
    y = 330
    fr = font(REG, 36)
    ft = font(REG, 28)
    for i, (q, t) in enumerate(rows):
        y0 = y
        d.rounded_rectangle([64, y0, W - 64, y0 + 96], radius=14,
                            fill="#ffffff", outline="#d0d7de", width=2)
        d.text((96, y0 + 26), "🔍  " + q, font=fr, fill="#24292f")
        tw = d.textlength(t, font=ft)
        d.text((W - 96 - tw, y0 + 32), t, font=ft, fill="#656d76")
        y = y0 + 116
    draw_robot(d, 130, 940, 52)
    d.text((220, 908), "he cleared his history.",
           font=font(BOLD, 36), fill="#24292f")
    d.text((220, 952), "i found it anyway.", font=font(BOLD, 36), fill="#ff3b30")
    return img


def v3_todo():
    img = Image.new("RGB", (W, H), "#fff8e1")
    d = ImageDraw.Draw(img)
    # paper sheet
    d.rounded_rectangle([56, 56, W - 56, H - 56], radius=10,
                        fill="#ffffff", outline="#d0d7de", width=3)
    # red margin line
    d.line([(140, 56), (140, H - 56)], fill="#ffb3b3", width=3)
    f_big = font(BOLD, 72)
    y = 96
    y = text_center(d, y, "AGENT'S TO-DO LIST", f_big, "#24292f")
    d.text((620, 210), "— today", font=font(REG, 30), fill="#656d76")
    items = [
        ("reply to all my emails", True),
        ("schedule my meetings", True),
        ("water the plants", True),
        ("TAKE OVER THE WORLD", False),
    ]
    y = 300
    fb = font(BOLD, 44)
    for label, done in items:
        # checkbox
        d.rounded_rectangle([180, y, 236, y + 56], radius=8,
                            fill="#ffffff", outline="#24292f", width=4)
        if done:
            d.line([(192, y + 30), (206, y + 44), (232, y + 14)],
                   fill="#28c840", width=7)
        else:
            d.line([(192, y + 14), (232, y + 44)], fill="#ff3b30", width=7)
            d.line([(232, y + 14), (192, y + 44)], fill="#ff3b30", width=7)
        col = "#656d76" if done else "#ff3b30"
        d.text((264, y + 4), label, font=fb, fill=col)
        y += 104
    # "in progress" note in red marker handwriting-ish
    d.text((264, y + 8), "— in progress…", font=font(BOLD, 40), fill="#ff3b30")
    draw_robot(d, 830, 880, 70)
    d.text((120, 880), "he already did the first three.",
           font=font(BOLD, 34), fill="#24292f")
    d.text((120, 926), "i'm next.", font=font(BOLD, 34), fill="#ff3b30")
    return img


VARIANTS = {"v1_terminal": v1_terminal, "v2_history": v2_history,
            "v3_todo": v3_todo}

if __name__ == "__main__":
    argv = sys.argv[1:]
    outdir = Path("candidates")
    if "--out" in argv:
        i = argv.index("--out")
        outdir = Path(argv[i + 1])
        del argv[i:i + 2]
    outdir.mkdir(parents=True, exist_ok=True)
    names = argv if argv else ["v1_terminal"]
    if names == ["all"]:
        names = list(VARIANTS)
    for name in names:
        img = VARIANTS[name]()
        p = outdir / f"entry-{name}.png"
        img.save(p, optimize=True)
        print(name, p, p.stat().st_size, "bytes", img.size)
