#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rosehip Hedge Theme — vector logo candidates (SVG, headless Chromium).

Style: solid fill only, **no outlines anywhere** (user request 2026-11-01). Because
every palette colour is pale, separation comes from three devices instead of a
stroke:

  * light fill layered on a darker fill (blush berry on deep sage)
  * the darkest tone (#2F3B2E) used as the silhouette itself
  * one soft drop shadow so the mark lifts off an ivory page

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
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
BLUSH = hx(_C["toolbar"])                          # #F6E2E9
IVORY = hx(_C["ntp_background"])                   # #FEFAF3
INK = hx(_C["ntp_text"])                           # #2F3B2E
LINK = hx(_C["ntp_link"])                          # #4E6B4C
BERRY = "#D98CA6"                                  # deepened blush for the hips
BERRY_DEEP = "#C1708C"

SHADOW = """
  <filter id="ds" x="-35%%" y="-35%%" width="170%%" height="170%%">
    <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="%s" flood-opacity=".20"/>
  </filter>""" % INK


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


def berry(cx, cy, r, fill, hi=True):
    """Solid hip: body + a soft highlight, no outline."""
    out = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, fill)
    if hi:
        out += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF" fill-opacity=".42"/>'
                % (cx - r * 0.30, cy - r * 0.32, r * 0.26))
    return out


def leaf(cx, cy, rx, ry, angle, fill):
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
            'transform="rotate(%.1f %.1f %.1f)"/>' % (cx, cy, rx, ry, fill, angle, cx, cy))


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
</g>
""" % (SHADOW,
       leaf(96, 168, 46, 22, -30, SAGE),
       leaf(160, 168, 46, 22, 30, SAGE),
       berry(128, 116, 52, BERRY),
       '<circle cx="128" cy="70" r="13" fill="%s"/>' % BERRY_DEEP))

SVG_02 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <path d="M40 214 Q40 122 96 122 Q128 122 142 96 Q166 62 196 68 Q226 76 226 124 L226 214 Z"
        fill="%s"/>
  %s
  %s
  %s
</g>
""" % (SHADOW, DEEP,
       berry(84, 172, 20, BERRY),
       berry(136, 148, 24, BERRY),
       berry(184, 178, 18, BERRY)))

SVG_03 = svg_open("""
<defs>%s</defs>
<circle cx="128" cy="122" r="92" fill="%s" filter="url(#ds)"/>
%s
%s
%s
""" % (SHADOW, DEEP,
       leaf(94, 168, 38, 17, -26, IVORY),
       leaf(162, 168, 38, 17, 26, IVORY),
       berry(128, 110, 44, BERRY)))

SVG_04 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
</g>
""" % (SHADOW,
       leaf(128, 150, 30, 78, 0, SAGE),
       leaf(92, 168, 26, 62, -34, DEEP),
       leaf(164, 168, 26, 62, 34, DEEP),
       berry(128, 74, 34, BERRY)))

SVG_05 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <path d="M40 220 V128 a88 88 0 0 1 176 0 V220 Z" fill="%s"/>
  <path d="M76 220 V132 a52 52 0 0 1 104 0 V220 Z" fill="%s"/>
  %s
  %s
</g>
""" % (SHADOW, DEEP, IVORY,
       berry(108, 162, 17, BERRY),
       berry(150, 186, 14, BERRY)))

SVG_06 = svg_open("""
<defs>
  <linearGradient id="bd6" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M128 40 C170 78 196 118 196 152 C196 194 166 220 128 220 C90 220 60 194 60 152
           C60 118 86 78 128 40 Z" fill="url(#bd6)"/>
  %s
</g>
%s
""" % (BERRY, BERRY_DEEP, SHADOW,
       '<ellipse cx="104" cy="146" rx="16" ry="24" fill="#FFFFFF" fill-opacity=".35" '
       'transform="rotate(-18 104 146)"/>',
       leaf(150, 196, 44, 18, 24, SAGE)))

CANDIDATES = [
    ("01", "solid-hip", "One big hip over two sage leaves — flat, no outline", SVG_01),
    ("02", "hedge-swell", "Deep-sage hedge carrying three hips", SVG_02),
    ("03", "hip-disc", "Deep-sage disc, blush hip, ivory leaves", SVG_03),
    ("04", "leaf-fan", "Three leaves fanning under one hip", SVG_04),
    ("05", "arch-hedge", "Sage arch hedge with hips inside", SVG_05),
    ("06", "hip-drop", "Gradient hip over a single leaf — softest", SVG_06),
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
