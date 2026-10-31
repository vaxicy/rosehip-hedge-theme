#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rosehip Hedge Theme — flat vector logo candidates (SVG, headless Chromium).

v4 direction (user request 2026-11-01): **flat and simple** — solid fills only,
no gradients, no highlights, no outlines, no shadows. Two or three shapes per mark,
sized so they still read at 32px.

Because nothing adds depth, the shapes themselves must carry the contrast: the
foliage uses the two darkest palette tones (deep sage / link) and the hips a
deepened blush, all of which sit clearly on an ivory page.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


SAGE = hx(_C["frame"])                             # #B8CFB3
DEEP = hx(_C["button_background"])                 # #84A282
IVORY = hx(_C["ntp_background"])                   # #FEFAF3
INK = hx(_C["ntp_text"])                           # #2F3B2E
LINK = hx(_C["ntp_link"])                          # #4E6B4C
HIP = "#D98CA6"                                    # deepened blush for the hips


def svg_open(body, defs=""):
    # 0.94 about the centre keeps every mark inside the safe box
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s<g transform="translate(128 128) scale(0.94) '
            'translate(-128 -128)">%s</g></svg>' % (CELL, CELL, defs, body))


def leaf(cx, cy, length, width, angle, fill):
    """Flat leaf: two arcs meeting at the tip, base at (0,0). No vein, no stroke."""
    half = length * 0.5
    d = ("M0 0 C %.1f %.1f %.1f %.1f 0 %.1f C %.1f %.1f %.1f %.1f 0 0 Z"
         % (width, -half * 0.55, width * 0.86, -half * 1.25, -length,
            -width * 0.86, -half * 1.25, -width, -half * 0.55))
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)"><path d="%s" fill="%s"/></g>'
            % (cx, cy, angle, d, fill))


def hip(cx, cy, r, fill=HIP):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, fill)


def stem(d, width, color=LINK):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
            % (d, color, width))


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
%s
%s
%s
""" % (       leaf(84, 214, 88, 36, 24, DEEP),
       leaf(172, 214, 88, 36, -24, DEEP),
       hip(128, 116, 58)))

SVG_02 = svg_open("""
%s
%s
%s
%s
""" % ('<path d="M34 200 Q34 96 128 96 Q222 96 222 200 Z" fill="%s"/>' % DEEP,
       hip(94, 152, 22),
       hip(160, 168, 17),
       leaf(126, 96, 54, 20, 0, SAGE)))

SVG_03 = svg_open("""
%s
%s
%s
""" % ('<circle cx="128" cy="126" r="94" fill="%s"/>' % DEEP,
       leaf(128, 188, 96, 38, 0, IVORY),
       hip(128, 112, 52)))

SVG_04 = svg_open("""
%s
%s
%s
""" % (       leaf(102, 200, 92, 36, 26, SAGE),
       leaf(154, 200, 92, 36, -26, DEEP),
       hip(128, 92, 42)))

SVG_05 = svg_open("""
%s
%s
%s
""" % ('<path d="M44 214 V132 a84 84 0 0 1 168 0 V214 Z" fill="%s"/>' % DEEP,
       '<path d="M80 214 V136 a48 48 0 0 1 96 0 V214 Z" fill="%s"/>' % IVORY,
       hip(128, 176, 26)))

SVG_06 = svg_open("""
%s
%s
%s
%s
""" % (hip(128, 84, 38),
       hip(88, 150, 30),
       hip(168, 150, 30),
       leaf(128, 214, 66, 26, 0, SAGE)))

CANDIDATES = [
    ("01", "hip-leaf", "One hip between two leaves — simplest read", SVG_01),
    ("02", "hedge-dome", "A sage hedge dome with two hips", SVG_02),
    ("03", "hip-disc", "Hip on a sage disc with one ivory leaf", SVG_03),
    ("04", "leaf-pair", "Two leaves under one hip", SVG_04),
    ("05", "arch-hedge", "Hedge arch with a hip in the opening", SVG_05),
    ("06", "hip-trio", "Three hips over a leaf", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=INK)
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (254, 250, 243), (47, 59, 46), (128, 142, 126),
                  CAND_DIR / "contact-light.png", "Rosehip Hedge — flat candidates (light)")
    contact_sheet(rendered, (40, 50, 40), (246, 226, 233), (150, 168, 148),
                  CAND_DIR / "contact-dark.png", "Rosehip Hedge — flat candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
