#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rosehip Hedge Theme — promo tiles (440x280 + 1400x560), all English.

  1400x560 · window hero — deep olive ground with a rounded browser-window card.
  440x280  · dot palette — centred stack with five colour dots.

Colours are read from manifest.json. Every layout ends with bounds assertions so
overflow fails loudly at generation time.
"""
import json
import os
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

OUT_DIR = "store-assets/promo"
INK = (34, 48, 58)
WHITE = (255, 255, 255)
# Chrome draws the caption buttons on a block darker than the tab strip
CAPTION = (143, 171, 140)
SHELL = (255, 253, 246)

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]

FRAME = tuple(_C["frame"])
TOOLBAR = tuple(_C["toolbar"])
PAGE = tuple(_C["ntp_background"])
BTN = tuple(_C["button_background"])
BTN2 = tuple(_C["button_background_secondary"])
INK_T = tuple(_C["ntp_text"])
LINK = tuple(_C["ntp_link"])
CREAM = tuple(_C["button_background_secondary"])
DEEP = tuple(_C["ntp_text"])             # deep plum used as the dark ground
DEEP_END = tuple(min(255, int(v * 1.32)) for v in DEEP)
LOGO_ROSE = (243, 193, 105)               # derived single-colour logo on this palette
DISC = (246, 212, 151)


def save_png(img, path, tries=5):
    """PIL intermittently raises OSError [Errno 22] on this non-ASCII path."""
    last = None
    for i in range(tries):
        try:
            img.save(path)
            return
        except OSError as exc:            # pragma: no cover - environment specific
            last = exc
            time.sleep(0.35 * (i + 1))
    raise last


def font(size, bold=False):
    win = os.environ.get("WINDIR", r"C:\Windows")
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(win, "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def draw_chip(d, x, y, h, label, f, fill, txt, pad=16, outline=None):
    w = text_w(d, label, f) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill, outline=outline, width=1)
    d.text((x + pad, y + (h - f.size) // 2 - 3), label, font=f, fill=txt)
    return w


def cta(d, x, y, w, h, bg, fg, label="Try It Now"):
    f = font(20, True)
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + (w - text_w(d, label, f)) // 2, y + (h - f.size) // 2 - 3), label, font=f, fill=fg)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ------------------------------------------------- 1400x560: window hero
def compose_window(size=(1400, 560)):
    W, H = size
    M = 70
    RIGHT = W - M

    img = Image.new("RGB", (W, H), DEEP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(DEEP, DEEP_END, y / max(1, H - 1)))

    # ---- browser window card
    wx0, wy0, wx1, wy1 = 740, 84, 1330, 476
    assert wx1 <= RIGHT and wy1 <= H - 60, "window card overflows"
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([wx0, wy0 + 14, wx1, wy1 + 14], radius=18,
                                             fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    # the mini window mirrors the real one: sage tab strip with a darker caption
    # block, blush toolbar carrying the omnibox, blush bookmark bar, then the page
    d.rounded_rectangle([wx0, wy0, wx1, wy1], radius=18, fill=PAGE)
    d.rounded_rectangle([wx0, wy0, wx1, wy0 + 34], radius=18, fill=FRAME)
    d.rectangle([wx0, wy0 + 20, wx1, wy0 + 34], fill=FRAME)
    for i, lab in enumerate(("Color", "Theme", "New Tab")):
        x = wx0 + 16 + i * 104
        d.rounded_rectangle([x, wy0 + 7, x + 92, wy0 + 28], radius=7,
                            fill=TOOLBAR if i == 2 else lerp(FRAME, WHITE, 0.38))
        d.text((x + 10, wy0 + 11), lab, font=font(11), fill=INK_T)
    # caption panel (three divided cells, dark glyphs) — matches the real window
    cap_w = 114
    cap_x0 = wx1 - cap_w
    d.rectangle([cap_x0, wy0, wx1, wy0 + 34], fill=CAPTION)
    for i in (1, 2):
        d.line([(cap_x0 + i * cap_w / 3, wy0), (cap_x0 + i * cap_w / 3, wy0 + 34)],
               fill=lerp(CAPTION, INK_T, 0.18), width=1)
    for i, glyph in enumerate(("\u2212", "\u25a1", "\u00d7")):
        d.text((cap_x0 + cap_w / 6 + i * cap_w / 3, wy0 + 10), glyph,
               font=font(12), fill=INK_T, anchor="ma")
    # toolbar band with the omnibox pill
    d.rectangle([wx0, wy0 + 34, wx1, wy0 + 74], fill=TOOLBAR)
    d.rounded_rectangle([wx0 + 16, wy0 + 42, wx1 - 16, wy0 + 68], radius=13, fill=WHITE)
    d.text((wx0 + 32, wy0 + 49), "Search Google or type a URL", font=font(11),
           fill=(120, 110, 125))
    # bookmark bar
    d.rectangle([wx0, wy0 + 74, wx1, wy0 + 94], fill=TOOLBAR)
    for i, lab in enumerate(("Folders", "Favorites", "Downloads", "Dev")):
        d.text((wx0 + 26 + i * 92, wy0 + 80), lab, font=font(10),
               fill=lerp(TOOLBAR, INK_T, 0.58))
    g = font(58, True)
    d.text((wx0 + (wx1 - wx0 - text_w(d, "Google", g)) // 2, wy0 + 118), "Google", font=g,
           fill=LOGO_ROSE)
    d.rounded_rectangle([wx0 + 66, wy0 + 214, wx1 - 66, wy0 + 248], radius=17, fill=WHITE)
    d.text((wx0 + 90, wy0 + 222), "Search Google or type a URL", font=font(12),
           fill=(120, 110, 125))
    # shortcut row: three discs only (no label row — user request 2026-10-23),
    # group centred in the card and verified by its real rendered extent
    r_disc, step = 26, 118
    card_mid = wx0 + (wx1 - wx0) / 2
    for i in range(3):
        cx = card_mid + (i - 1) * step
        d.ellipse([cx - r_disc, wy0 + 288, cx + r_disc, wy0 + 340], fill=DISC)
    group_left = card_mid - step - r_disc
    group_right = card_mid + step + r_disc
    assert abs((group_left - wx0) - (wx1 - group_right)) < 1.0, "disc group not centred in card"

    # ---- left column
    lg = Image.open("logo/logo.png").convert("RGBA").resize((120, 120), Image.LANCZOS)
    img.paste(lg, (M, 78), lg)
    d = ImageDraw.Draw(img)

    f_title = font(58, True)
    d.text((M + 144, 96), "Rosehip Hedge", font=f_title, fill=SHELL)
    assert M + 144 + text_w(d, "Rosehip Hedge", f_title) <= wx0 - 30, "title collides with card"
    d.text((M + 146, 174), "A soft spring Chrome theme", font=font(21),
           fill=lerp(SHELL, DEEP, 0.26))

    f_chip = font(15)
    cx, cy = M + 146, 214
    for lab in ("Solid colors", "Soft spring", "Easy on the eyes"):
        # cream pill + plum ink: cream-on-cream would be invisible on the dark ground
        cx += draw_chip(d, cx, cy, 34, lab, f_chip, SHELL, DEEP) + 12
    assert cx - 12 <= wx0 - 24, "chip row collides with card"

    # no swatch legend here: two of the five tones are near-black and would vanish
    # into this dark ground (same call as shadow-glade); the card carries the palette.

    # CTA bottom-aligned with the window card so the left column spans the same band
    cta_y = wy1 - 54
    cta(d, M, cta_y, 210, 54, SHELL, DEEP)
    assert cta_y > cy + 34 + 30, "CTA collides with the chip row"
    assert cta_y + 54 <= H - 24, "CTA too close to the bottom"
    return img, {"card": (wx0, wy0, wx1 - wx0, wy1 - wy0), "cta": (M, cta_y, 210, 54)}


# ------------------------------------------------- 440x280: dot palette
def compose_dots(size=(440, 280)):
    W, H = size
    M = 28
    bg = PAGE
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    lsize = 60
    logo = Image.open("logo/logo.png").convert("RGBA").resize((lsize, lsize), Image.LANCZOS)
    img.paste(logo, ((W - lsize) // 2, 22), logo)
    d = ImageDraw.Draw(img)

    f_title, f_sub = font(27, True), font(12)
    title = "Rosehip Hedge"
    d.text(((W - text_w(d, title, f_title)) // 2, 92), title, font=f_title, fill=INK_T)
    sub = "A soft spring Chrome theme"
    d.text(((W - text_w(d, sub, f_sub)) // 2, 126), sub, font=f_sub, fill=lerp(INK_T, bg, 0.32))

    # five distinct tones ordered light -> dark so the row reads as a ramp and the
    # two near-blacks do not clump together
    dots = [tuple(_C["ntp_text"]), tuple(_C["ntp_link"]), BTN, FRAME, BTN2]
    r, gap = 11, 14
    total = len(dots) * 2 * r + (len(dots) - 1) * gap
    x0 = (W - total) // 2
    y0 = 172
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i in range(len(dots)):
        cx = x0 + i * (2 * r + gap) + r
        sd.ellipse([cx - r, y0 - r + 3, cx + r, y0 + r + 3], fill=INK_T + (34,))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)
    # hairline ring: the bone dot would otherwise disappear into the bone page
    ring = lerp(INK_T, bg, 0.80)
    for i, col in enumerate(dots):
        cx = x0 + i * (2 * r + gap) + r
        d.ellipse([cx - r, y0 - r, cx + r, y0 + r], fill=col, outline=ring, width=1)
    assert x0 >= M and x0 + total <= W - M, "dot row overflows"

    f_cta = font(13, True)
    cw, ch = 128, 34
    bx, by = (W - cw) // 2, 206
    d.rounded_rectangle([bx, by, bx + cw, by + ch], radius=ch // 2, fill=DEEP)
    label = "Try It Now"
    d.text((bx + (cw - text_w(d, label, f_cta)) // 2, by + (ch - f_cta.size) // 2 - 3),
           label, font=f_cta, fill=SHELL)
    assert by + ch <= H - M, "CTA too close to the bottom"
    return img, {"dots": (x0, y0 - r, total, 2 * r), "cta": (bx, by, cw, ch)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for compose, name in ((compose_window, "1400x560.png"), (compose_dots, "440x280.png")):
        img, boxes = compose()
        out = "%s/%s" % (OUT_DIR, name)
        save_png(img, out)
        print("saved:", out, img.size, img.mode, boxes)


if __name__ == "__main__":
    main()
