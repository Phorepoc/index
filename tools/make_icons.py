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
    "qt-symbian-arm": ("cube", A["maps"]),
    "codecpack-arm": ("play", A["videos"]), "codecpack-x32": ("play", A["videos"]),
}

if __name__ == "__main__":
    for lid, (glyph, accent) in sorted(ICONS.items()):
        folder = os.path.join(ROOT, "listings", lid)
        with open(os.path.join(folder, "icon.svg"), "w", newline="\n") as f:
            f.write(icongen.svg(icongen.GLYPHS[glyph], accent, lid))
        icongen.render_png(icongen.GLYPHS[glyph], accent, 256).save(os.path.join(folder, "icon.png"))
        print("icon:", lid, glyph, accent)
