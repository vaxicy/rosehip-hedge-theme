#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rosehip Hedge Theme — vector logo candidates (SVG, headless Chromium).

v3 direction: botanical illustration rather than flat pictogram. Every mark is
built from real leaf geometry (two quadratic arcs meeting at a point), rosehips
with their calyx star, and layered depth — gradient fill + drop shadow + a
soft highlight — with **no outline strokes around the shapes**.

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
HIP = "#D98CA6"
HIP_DARK = "#BC6F89"

SHADOW = """
  <filter id="ds" x="-40%%" y="-40%%" width="180%%" height="180%%">
    <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="%s" flood-opacity=".22"/>
  </filter>""" % INK

SOFT = """
  <filter id="sf" x="-40%%" y="-40%%" width="180%%" height="180%%">
    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="%s" flood-opacity=".16"/>
  </filter>""" % INK


def svg_open(body, defs=""):
    # 0.93 about the centre keeps every mark (plus its drop shadow) inside the
    # 24-232 safe box without hand-tuning each composition
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s<g transform="translate(128 128) scale(0.93) '
            'translate(-128 -128)">%s</g></svg>' % (CELL, CELL, defs, body))


def leaf(cx, cy, length, width, angle, fill, vein=None, opacity=1.0):
    """A real leaf: two quadratic arcs meeting at the tip, base at (0,0)."""
    half = length * 0.5
    d = ("M0 0 C %.1f %.1f %.1f %.1f 0 %.1f C %.1f %.1f %.1f %.1f 0 0 Z"
         % (width, -half * 0.55, width * 0.86, -half * 1.25, -length,
            -width * 0.86, -half * 1.25, -width, -half * 0.55))
    out = ('<g transform="translate(%.1f %.1f) rotate(%.1f)" opacity="%.2f">' % (cx, cy, angle, opacity))
    out += '<path d="%s" fill="%s"/>' % (d, fill)
    if vein:
        out += ('<path d="M0 -2 L0 %.1f" stroke="%s" stroke-width="2.2" stroke-opacity=".38" '
                'stroke-linecap="round"/>' % (-length * 0.88, vein))
        for i in range(1, 4):
            ty = -length * (0.16 + 0.2 * i)
            spread = width * (0.85 - 0.13 * i)
            out += ('<path d="M0 %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="1.6" '
                    'stroke-opacity=".28" fill="none" stroke-linecap="round"/>'
                    % (ty, spread * 0.5, ty - length * 0.06, spread, ty - length * 0.16, vein))
            out += ('<path d="M0 %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="1.6" '
                    'stroke-opacity=".28" fill="none" stroke-linecap="round"/>'
                    % (ty, -spread * 0.5, ty - length * 0.06, -spread, ty - length * 0.16, vein))
    out += "</g>"
    return out


def hip(cx, cy, r, gid, calyx=True, hi=True):
    """Rosehip: gradient body, five-sepal star on top, soft highlight."""
    out = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#%s)"/>' % (cx, cy, r, gid)
    if calyx:
        for i in range(5):
            a = math.radians(-90 + (i - 2) * 26)
            x2 = cx + r * 1.24 * math.cos(a)
            y2 = cy + r * 1.10 * math.sin(a)
            out += ('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" opacity=".9"/>'
                    % (cx + r * 0.16 * math.cos(a + 1.2), cy + r * 0.16 * math.sin(a + 1.2),
                       x2, y2,
                       cx + r * 0.16 * math.cos(a - 1.2), cy + r * 0.16 * math.sin(a - 1.2),
                       LINK))
    if hi:
        out += ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#FFFFFF" '
                'fill-opacity=".40" transform="rotate(-22 %.1f %.1f)"/>'
                % (cx - r * 0.34, cy - r * 0.36, r * 0.30, r * 0.20, cx - r * 0.34, cy - r * 0.36))
    return out


def stem(d, width, color, opacity=1.0):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" '
            'stroke-opacity="%.2f"/>' % (d, color, width, opacity))


HIPGRAD = """
    <radialGradient id="hg1" cx="34%%" cy="28%%" r="78%%">
      <stop offset="0" stop-color="#F0AEC4"/>
      <stop offset="0.62" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </radialGradient>
    <radialGradient id="hg2" cx="36%%" cy="30%%" r="76%%">
      <stop offset="0" stop-color="#E9A0BA"/>
      <stop offset="0.66" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </radialGradient>
    <linearGradient id="lg1" x1="0" y1="1" x2="0.4" y2="0">
      <stop offset="0" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </linearGradient>
    <linearGradient id="lg2" x1="0" y1="1" x2="0.3" y2="0">
      <stop offset="0" stop-color="%s"/>
      <stop offset="1" stop-color="%s"/>
    </linearGradient>""" % (HIP, HIP_DARK, HIP, HIP_DARK, DEEP, SAGE, LINK, DEEP)

# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>%s%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
  %s
  %s
  %s
</g>
""" % (HIPGRAD, SHADOW,
       leaf(126, 178, 52, 21, 168, "url(#lg1)", INK),
       leaf(126, 160, 50, 20, 132, "url(#lg2)", INK),
       leaf(126, 144, 48, 19, 62, "url(#lg2)", INK),
       leaf(126, 126, 46, 18, 100, "url(#lg1)", INK),
       stem("M126 186 C124 158 122 132 126 104", 5.0, LINK),
       hip(126, 82, 28, "hg1"),
       hip(86, 118, 17, "hg2")))

SVG_02 = svg_open("""
<defs>%s%s</defs>
<circle cx="128" cy="124" r="94" fill="%s" filter="url(#ds)"/>
<g filter="url(#sf)">
  <path d="M56 196 V132 a72 72 0 0 1 144 0 V196 Z" fill="%s"/>
  <path d="M56 196 V132 a72 72 0 0 1 144 0 Z" fill="%s" opacity=".5"/>
</g>
%s
%s
%s
%s
%s
""" % (HIPGRAD, SHADOW, DEEP, IVORY, SAGE,
       hip(108, 150, 20, "hg1", calyx=False),
       hip(150, 164, 15, "hg2", calyx=False),
       leaf(92, 196, 30, 12, 200, SAGE),
       leaf(164, 196, 30, 12, 160, SAGE),
       stem("M128 196 C128 176 128 166 128 158", 3.4, LINK)))

SVG_03 = svg_open("""
<defs>%s%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
  %s
</g>
""" % (HIPGRAD, SHADOW,
       leaf(128, 178, 58, 24, 172, "url(#lg1)", INK),
       leaf(128, 178, 52, 21, 8, "url(#lg2)", INK),
       stem("M128 186 C126 166 126 152 128 140", 5.0, LINK),
       hip(128, 104, 42, "hg1"),
       hip(176, 72, 20, "hg2")))

SVG_04 = svg_open("""
<defs>%s%s</defs>
<g filter="url(#ds)">
  <path d="M28 200 Q28 150 74 150 Q104 150 116 128 Q132 100 164 104 Q200 108 210 152 Q216 176 216 200 Z"
        fill="%s"/>
  <path d="M28 200 Q28 168 60 160 Q96 152 118 172 Q146 196 176 178 Q204 162 216 178 L216 200 Z"
        fill="%s"/>
  %s
  %s
  %s
  %s
</g>
""" % (HIPGRAD, SHADOW, SAGE, DEEP,
       hip(92, 176, 17, "hg1", calyx=False),
       hip(140, 186, 14, "hg2", calyx=False),
       hip(180, 168, 15, "hg1", calyx=False),
       leaf(60, 196, 34, 13, 176, "url(#lg1)", INK)))

SVG_05 = svg_open("""
<defs>%s%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
  %s
</g>
""" % (HIPGRAD, SHADOW,
       leaf(94, 188, 46, 19, 196, "url(#lg2)", INK),
       leaf(162, 188, 46, 19, 164, "url(#lg1)", INK),
       stem("M128 194 C126 178 126 166 128 154", 4.6, LINK),
       hip(128, 110, 54, "hg1"),
       hip(184, 58, 15, "hg2")))

SVG_06 = svg_open("""
<defs>%s%s</defs>
<g filter="url(#ds)">
  %s
  %s
  %s
  %s
  %s
  %s
</g>
""" % (HIPGRAD, SHADOW,
       stem("M60 214 C76 176 96 148 128 138 C160 148 180 176 196 214", 8.0, LINK),
       leaf(84, 178, 44, 18, 214, "url(#lg1)", INK),
       leaf(172, 178, 44, 18, 146, "url(#lg2)", INK),
       leaf(72, 208, 38, 15, 236, "url(#lg2)", INK, 0.95),
       leaf(184, 208, 38, 15, 124, "url(#lg1)", INK, 0.95),
       hip(128, 120, 27, "hg1")))

CANDIDATES = [
    ("01", "hip-branch", "Botanical hip branch — four leaves, two hips", SVG_01),
    ("02", "hedge-arch", "Ivory arch in a sage badge with hips and leaves", SVG_02),
    ("03", "hip-duo", "Two hips with a leaf pair at the base", SVG_03),
    ("04", "hedge-bed", "Layered hedge bed with three hips", SVG_04),
    ("05", "hero-hip", "One large hero hip over two leaves", SVG_05),
    ("06", "bramble-arch", "A branch bent into an arch holding a hip", SVG_06),
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
                  CAND_DIR / "contact-light.png", "Rosehip Hedge — botanical candidates (light)")
    contact_sheet(rendered, (40, 50, 40), (246, 226, 233), (150, 168, 148),
                  CAND_DIR / "contact-dark.png", "Rosehip Hedge — botanical candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
