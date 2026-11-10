# Copyright The Phorepoc Authors
# SPDX-License-Identifier: Apache-2.0
"""make_icons.py -- (re)draws the listing icons to the Etesian design language (icongen.py): for each listing the SVG
source (icon.svg) and the 256 x 256 PNG the index schema asks for (icon.png). Run: python3 tools/make_icons.py
Needs Pillow. A new listing's icon is one line in ICONS: its glyph (icongen.GLYPHS) and its accent (icongen.ACCENTS)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icongen  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = icongen.ACCENTS
ICONS = {
    "webkit-symbian-arm": ("cog", A["browser"]), "webkit-symbian-x32": ("cog", A["browser"]),
    "netsurf-symbian-arm": ("compass", A["browser"]), "netsurf-symbian-x32": ("compass", A["browser"]),
    "qt-symbian-arm": ("cube", A["maps"]), "qt-symbian-x32": ("cube", A["maps"]),
    "orbit-ui-x32": ("globe", A["photos"]),
    "codecpack-arm": ("play", A["videos"]), "codecpack-x32": ("play", A["videos"]),
    "screenrec-a64-arm": ("record", A["videos"]),
    "dav-sync-arm": ("sync", A["contacts"]), "dav-sync-x32": ("sync", A["contacts"]),
    "tailscale-symbian-arm": ("tunnel", A["conversations"]), "tailscale-symbian-x32": ("tunnel", A["conversations"]),
}

# One icon per tag of the fixed vocabulary (CONTRIBUTING.md): categories/<tag, spaces as dashes>.png (128 x 128) + .svg.
# The glyphs are drawn here on the same 24 grid (icongen's rules: one 2 px round stroke).
CAT_GLYPHS = {
    "chip": [("rrect", 6, 6, 12, 12, 2), ("rrect", 9.5, 9.5, 5, 5, 1)] + [("line", [(x, 2.5), (x, 6)]) for x in (9, 15)]
    + [("line", [(x, 18), (x, 21.5)]) for x in (9, 15)] + [("line", [(2.5, y), (6, y)]) for y in (9, 15)]
    + [("line", [(18, y), (21.5, y)]) for y in (9, 15)],
    "pad": [("rrect", 2.5, 7, 19, 11, 5), ("line", [(7, 12.5), (11, 12.5)]), ("line", [(9, 10.5), (9, 14.5)]),
            ("dot", 15.5, 11.5), ("dot", 18, 14)],
    "brush": [("circle", 12, 12, 9), ("dot", 8, 9.5), ("dot", 12.5, 7), ("dot", 16.5, 10), ("circle", 13.5, 15, 2.2)],
    "wrench": [("line", [(4.5, 19.5), (13.5, 10.5)]), ("circle", 16.5, 7.5, 4), ("line", [(14, 10), (16, 12)])],
    "note": [("line", [(9, 17), (9, 5), (19, 3), (19, 15)]), ("circle", 6.5, 17.5, 2.5), ("circle", 16.5, 15.5, 2.5)],
    "picture": [("rrect", 3, 4.5, 18, 15, 2), ("circle", 8.5, 9.5, 1.8),
                ("line", [(3.5, 17), (9, 12.5), (13, 16), (16, 13.5), (20.5, 17.5)])],
    "nodes": [("circle", 12, 5, 2.6), ("circle", 5, 18, 2.6), ("circle", 19, 18, 2.6),
              ("line", [(11, 7.4), (6, 15.6)]), ("line", [(13, 7.4), (18, 15.6)]), ("line", [(7.6, 18), (16.4, 18)])],
    "shield": [("poly", [(12, 2.8), (20, 6), (20, 12), (12, 21.2), (4, 12), (4, 6)]),
               ("line", [(8.5, 11.5), (11, 14), (15.5, 9)])],
    "pad2": [("rrect", 5, 3, 14, 18, 2), ("line", [(8.5, 8), (15.5, 8)]), ("line", [(8.5, 12), (15.5, 12)]),
             ("line", [(8.5, 16), (12.5, 16)])],
    "sliders": [("line", [(4, 7), (20, 7)]), ("line", [(4, 17), (20, 17)]), ("circle", 9, 7, 2.4), ("circle", 15, 17, 2.4)],
}
G = icongen.GLYPHS
CATEGORIES = {
    "browser engine": (G["cog"], A["browser"]), "library": (G["cube"], A["maps"]), "codec": (G["play"], A["videos"]),
    "driver": (CAT_GLYPHS["chip"], A["calculator"]), "game": (CAT_GLYPHS["pad"], A["phone"]),
    "theme": (CAT_GLYPHS["brush"], A["music"]), "tool": (CAT_GLYPHS["wrench"], A["clock"]),
    "media": (CAT_GLYPHS["note"], A["photos"]), "web": (G["globe"], A["browser"]),
    "graphics": (CAT_GLYPHS["picture"], A["calendar"]), "network": (CAT_GLYPHS["nodes"], A["conversations"]),
    "security": (CAT_GLYPHS["shield"], A["email"]), "productivity": (CAT_GLYPHS["pad2"], A["notes"]),
    "developer": (G["prompt"], A["store"]), "system": (CAT_GLYPHS["sliders"], A["contacts"]),
}


def category_file(tag):
    return tag.replace(" ", "-")


if __name__ == "__main__":
    for lid, (glyph, accent) in sorted(ICONS.items()):
        folder = os.path.join(ROOT, "listings", lid)
        with open(os.path.join(folder, "icon.svg"), "w", newline="\n") as f:
            f.write(icongen.svg(icongen.GLYPHS[glyph], accent, lid))
        icongen.render_png(icongen.GLYPHS[glyph], accent, 256).save(os.path.join(folder, "icon.png"))
        print("icon:", lid, glyph, accent)
    os.makedirs(os.path.join(ROOT, "categories"), exist_ok=True)
    for tag, (glyph, accent) in CATEGORIES.items():
        base = os.path.join(ROOT, "categories", category_file(tag))
        with open(base + ".svg", "w", newline=chr(10)) as f:
            f.write(icongen.svg(glyph, accent, tag))
        icongen.render_png(glyph, accent, 128).save(base + ".png")
        print("category icon:", tag)
