#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rosehip Hedge Theme — vector logo candidates (SVG rendered by headless Chromium).

The reference palette is four horizontal bands: blush, ivory, light sage, deep sage.
Rosehips have no red in that set, so the berries are drawn in a deepened blush and
the foliage in the two sages — the mark stays inside the palette while still
reading as "hedge with hips".

Every palette colour is pale, so each mark pairs a pale fill with a deep olive
outline; without the outline the shapes vanish on the ivory page.

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
DEEP_SAGE = hx(_C["button_background"])            # #84A282
BLUSH = hx(_C["toolbar"])                          # #F6E2E9
IVORY = hx(_C["ntp_background"])                   # #FEFAF3
INK = hx(_C["ntp_text"])                           # #2F3B2E
LINK = hx(_C["ntp_link"])                          # #4E6B4C
BERRY = "#E2A0B4"                                  # deepened blush for the hips

SHADOW = """
  <filter id="ds" x="-35%%" y="-35%%" width="170%%" height="170%%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="%s" flood-opacity=".18"/>
  </filter>""" % INK


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


def simple_berry(cx, cy, r, fill):
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="3"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF" fill-opacity=".45"/>'
            % (cx, cy, r, fill, INK, cx - r * 0.3, cy - r * 0.35, r * 0.26))


def leaf(cx, cy, rx, ry, angle, fill, vein=True):
    out = ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" '
           'stroke-width="3" transform="rotate(%.1f %.1f %.1f)"/>'
           % (cx, cy, rx, ry, fill, INK, angle, cx, cy))
    if vein:
        out += ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="2.4" '
                'stroke-opacity=".45" transform="rotate(%.1f %.1f %.1f)"/>'
                % (cx - rx * 0.7, cy, cx + rx * 0.7, cy, INK, angle, cx, cy))
    return out


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <path d="M128 226 C126 186 124 150 128 116" stroke="%s" stroke-width="7"
        stroke-linecap="round" fill="none"/>
  %s
  %s
  %s
  %s
  %s
</g>
""" % (SHADOW, LINK,
       leaf(96, 132, 30, 13, -32, SAGE),
       leaf(160, 150, 30, 13, 32, SAGE),
       simple_berry(128, 84, 21, BERRY),
       simple_berry(104, 108, 15, BERRY),
       simple_berry(152, 108, 15, BERRY)))

SVG_02 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <path d="M40 206 q20 -48 44 -48 q24 0 44 -22 q20 -22 44 -22 q24 0 44 44 v48 Z"
        fill="%s" stroke="%s" stroke-width="4"/>
  %s
  %s
  %s
</g>
""" % (SHADOW, SAGE, INK,
       simple_berry(84, 168, 13, BERRY),
       simple_berry(128, 140, 16, BERRY),
       simple_berry(174, 174, 13, BERRY)))

SVG_03 = svg_open("""
<defs>%s</defs>
<circle cx="128" cy="128" r="100" fill="%s" filter="url(#ds)"/>
%s
%s
%s
""" % (SHADOW, DEEP_SAGE,
       simple_berry(128, 118, 34, BERRY),
       leaf(94, 176, 32, 14, -28, BLUSH),
       leaf(162, 176, 32, 14, 28, BLUSH)))

SVG_04 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
</g>
""" % (SHADOW, leaf(128, 158, 62, 44, 90, SAGE),
       simple_berry(128, 128, 26, BERRY),
       simple_berry(104, 214, 13, BERRY)))

SVG_05 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <path d="M34 214 q0 -38 30 -38 q30 0 30 38 Z" fill="%s" stroke="%s" stroke-width="4"/>
  <path d="M96 214 q0 -50 40 -50 q40 0 40 50 Z" fill="%s" stroke="%s" stroke-width="4"/>
  <path d="M178 214 q0 -34 26 -34 q26 0 26 34 Z" fill="%s" stroke="%s" stroke-width="4"/>
  %s
  %s
</g>
""" % (SHADOW, SAGE, INK, DEEP_SAGE, INK, SAGE, INK,
       simple_berry(140, 132, 17, BERRY),
       simple_berry(62, 156, 12, BERRY)))

SVG_06 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <!-- hip cluster: three berries in a triangle over two leaves -->
  <path d="M88 176 Q128 158 168 176" fill="none" stroke="%s" stroke-width="6"
        stroke-linecap="round"/>
  %s
  %s
  %s
  %s
  %s
</g>
""" % (SHADOW, LINK,
       simple_berry(128, 96, 27, BERRY),
       simple_berry(92, 140, 21, BERRY),
       simple_berry(164, 140, 21, BERRY),
       leaf(96, 190, 30, 13, -24, SAGE),
       leaf(160, 190, 30, 13, 24, SAGE)))

CANDIDATES = [
    ("01", "hip-sprig", "Three hips on a sprig with two leaves — most literal", SVG_01),
    ("02", "hedge-line", "A hedge silhouette carrying three hips", SVG_02),
    ("03", "hip-badge", "Deep sage badge with a blush hip — strongest at 32px", SVG_03),
    ("04", "single-hip", "One big hip over a leaf — simplest mark", SVG_04),
    ("05", "hedge-row", "Three hedge humps with hips — reads as a hedge row", SVG_05),
    ("06", "hip-cluster", "Three hips clustered over two leaves — most compact", SVG_06),
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
                  CAND_DIR / "contact-light.png", "Rosehip Hedge — vector logo candidates (light)")
    contact_sheet(rendered, (40, 50, 40), (246, 226, 233), (150, 168, 148),
                  CAND_DIR / "contact-dark.png", "Rosehip Hedge — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
