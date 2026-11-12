# Copyright The Phorepoc Authors
# SPDX-License-Identifier: Apache-2.0

"""Tests of the PR gate and the listing validation (python3 -m unittest discover -s tests)."""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import build_index  # noqa: E402
import check_pr  # noqa: E402

GOOD = {
    "id": "hello", "name": "Hello", "category": "app", "license": "EPL-1.0",
    "source": {"type": "github", "repo": "someone/hello"}, "releases": ["v1.0"],
    "compatibility": {"arch": ["arm", "x32"]},
}


def gate(files, maintainer=False):
    sys.stdin = io.StringIO("\n".join(files) + "\n")
    sys.argv = ["check_pr"] + (["--maintainer"] if maintainer else [])
    out = io.StringIO()
    with redirect_stdout(out):
        rc = check_pr.main()
    sys.stdin = sys.__stdin__
    return rc, out.getvalue()


class Gate(unittest.TestCase):
    def test_one_listing_folder(self):
        self.assertEqual(gate(["listings/hello/listing.json", "listings/hello/icon.png"])[0], 0)

    def test_two_listings(self):
        rc, out = gate(["listings/hello/listing.json", "listings/other/listing.json"])
        self.assertEqual(rc, 1)
        self.assertIn("one listing per pull request", out)

    def test_generated_or_tools(self):
        for f in ("index.json", "tools/build_index.py", ".github/workflows/publish.yml", "schema/listing.schema.json",
                  "listings/hello/sub/x.png"):
            self.assertEqual(gate(["listings/hello/listing.json", f])[0], 1, f)

    def test_maintainer(self):
        self.assertEqual(gate(["index.json", "tools/check_pr.py"], maintainer=True)[0], 0)


class Listing(unittest.TestCase):
    def setUp(self):
        self.schema = json.load(open(build_index.SCHEMA, encoding="utf-8"))
        self.tmp = tempfile.mkdtemp()
        self.old = build_index.LISTINGS
        build_index.LISTINGS = self.tmp

    def tearDown(self):
        build_index.LISTINGS = self.old
        shutil.rmtree(self.tmp)

    def write(self, lid, listing, files=()):
        os.makedirs(os.path.join(self.tmp, lid))
        json.dump(listing, open(os.path.join(self.tmp, lid, "listing.json"), "w"))
        for f in files:
            open(os.path.join(self.tmp, lid, f), "wb").close()

    def test_good(self):
        self.write("hello", GOOD)
        self.assertEqual(build_index.load_listing("hello", self.schema)["name"], "Hello")

    def test_bad(self):
        cases = {
            "unknown field": dict(GOOD, colour="red"),
            "missing field": {k: v for k, v in GOOD.items() if k != "license"},
            "bad category": dict(GOOD, category="spaceship"),
            "bad arch": dict(GOOD, compatibility={"arch": ["mips"]}),
            "bad releases": dict(GOOD, releases="newest"),
            "folder name": dict(GOOD, id="other"),
            "missing icon": dict(GOOD, icon="icon.png"),
            "unknown tag": dict(GOOD, tags=["shiny"]),
            "duplicate tag": dict(GOOD, tags=["game", "game"]),
            "too many tags": dict(GOOD, tags=["game", "media", "web", "tool", "driver", "theme"]),
            "no tags": dict(GOOD, tags=[]),
            "text written here": dict(GOOD, summary="Says hello"),
            "bad text folder": dict(GOOD, source=dict(GOOD["source"], text="../x")),
        }
        for what, listing in cases.items():
            with self.subTest(what):
                lid = "hello-" + what.replace(" ", "-")
                listing = dict(listing)
                if what != "folder name":
                    listing["id"] = lid
                self.write(lid, listing)
                with self.assertRaises(build_index.Invalid):
                    build_index.load_listing(lid, self.schema)

    def test_latest_and_icon(self):
        self.write("hello", dict(GOOD, releases="latest", icon="icon.png"), files=["icon.png"])
        self.assertEqual(build_index.load_listing("hello", self.schema)["releases"], "latest")
    def test_tags(self):
        self.write("hello", dict(GOOD, tags=["browser engine", "web"]))
        self.assertEqual(build_index.load_listing("hello", self.schema)["tags"], ["browser engine", "web"])


class Repository(unittest.TestCase):
    """the listings that are in this repository: each has tags and a square PNG icon of at least 128 px"""

    def test_every_listing_has_tags_and_an_icon(self):
        schema = json.load(open(build_index.SCHEMA, encoding="utf-8"))
        for lid in sorted(d for d in os.listdir(build_index.LISTINGS) if os.path.isdir(os.path.join(build_index.LISTINGS, d))):
            with self.subTest(lid):
                item = build_index.load_listing(lid, schema)
                self.assertTrue(item.get("tags"), "no tags")
                self.assertIn("icon", item, "no icon")
                with open(os.path.join(build_index.LISTINGS, lid, item["icon"]), "rb") as f:
                    head = f.read(24)
                self.assertEqual(head[1:4], b"PNG")
                w, h = int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
                self.assertEqual(w, h)
                self.assertGreaterEqual(w, 128)


    def test_groups(self):
        """listings of one app (a group) share its name and category and differ in architecture"""
        schema = json.load(open(build_index.SCHEMA, encoding="utf-8"))
        groups = {}
        for lid in sorted(d for d in os.listdir(build_index.LISTINGS) if os.path.isdir(os.path.join(build_index.LISTINGS, d))):
            item = build_index.load_listing(lid, schema)
            groups.setdefault(item.get("group", lid), []).append(item)
        for g, items in groups.items():
            with self.subTest(g):
                self.assertEqual(len({i["name"] for i in items}), 1, "names differ")
                self.assertEqual(len({i["category"] for i in items}), 1, "categories differ")
                arches = [a for i in items for a in i["compatibility"]["arch"]]
                self.assertEqual(len(arches), len(set(arches)), "two listings for one architecture")
                for i in items:
                    self.assertNotRegex(i["name"], r"\((PC|phones)\)$")


class AuthorText(unittest.TestCase):
    """the summary and description come from the item's repo: the newest approved release, else the default branch"""
    LISTING = dict(GOOD, source={"type": "github", "repo": "someone/hello"})
    RESOLVED = [{"tag": "v1.0", "published": "2026-01-01T00:00:00Z"}, {"tag": "v1.1", "published": "2026-02-01T00:00:00Z"}]

    def fetch(self, files):
        asked = []

        def github(url):
            asked.append(url)
            if url in files:
                return files[url].encode("utf-8")
            raise build_index.urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        old, build_index.github = build_index.github, github
        try:
            return build_index.author_text(self.LISTING, self.RESOLVED), asked
        finally:
            build_index.github = old

    def test_newest_release(self):
        raw = "https://raw.githubusercontent.com/someone/hello/v1.1/catalogue/"
        (summary, desc), asked = self.fetch({raw + "summary.txt": "Says hello\n", raw + "description.md": "Hello.\n"})
        self.assertEqual((summary, desc), ("Says hello", "Hello.\n"))
        self.assertTrue(asked[0].startswith(raw))

    def test_default_branch_when_the_release_predates_it(self):
        raw = "https://raw.githubusercontent.com/someone/hello/HEAD/catalogue/"
        (summary, desc), _ = self.fetch({raw + "summary.txt": "Says hello"})
        self.assertEqual((summary, desc), ("Says hello", ""))

    def test_none(self):
        with self.assertRaises(build_index.Invalid):
            self.fetch({})

    def test_too_long(self):
        raw = "https://raw.githubusercontent.com/someone/hello/v1.1/catalogue/"
        with self.assertRaises(build_index.Invalid):
            self.fetch({raw + "summary.txt": "x" * 141})

    def test_plain(self):
        md = ("> FFmpeg is the leading\n> multimedia framework.\n>\n> -- [FFmpeg](https://ffmpeg.org)\n\n"
              "It is built as `pheffmpeg.dll`,\nloaded at **run** time.\n")
        self.assertEqual(build_index.plain(md),
                         "FFmpeg is the leading multimedia framework.\n\n— FFmpeg\n\n"
                         "It is built as pheffmpeg.dll, loaded at run time.")
        self.assertEqual(build_index.plain("Use `record_start` / `record_stop`, _not_ snake_case_name.\n"),
                         "Use record_start / record_stop, not snake_case_name.")


class Categories(unittest.TestCase):
    """the categories block of index.json, which the phone app relies on"""
    SCHEMA = json.load(open(build_index.SCHEMA, encoding="utf-8"))

    def test_counts_order_and_icons(self):
        items = [{"tags": ["media", "codec"], "category": "codec"}, {"tags": ["web"], "category": "game"},
                 {"tags": ["browser engine", "web"], "category": "app"}]
        cats = build_index.categories(items, self.SCHEMA)
        self.assertEqual([c["tag"] for c in cats], ["browser engine", "codec", "game", "media", "web"])  # vocabulary order
        self.assertEqual({c["tag"]: c["count"] for c in cats}, {"browser engine": 1, "codec": 1, "game": 1, "media": 1, "web": 2})
        self.assertEqual(cats[0]["name"], "Browser engines")
        self.assertTrue(cats[0]["icon_url"].endswith("/categories/browser-engine.png"))
        self.assertEqual(set(cats[0]), {"tag", "name", "count", "icon_url"})

    def test_every_vocabulary_tag_has_an_icon(self):
        for tag in self.SCHEMA["properties"]["tags"]["items"]["enum"]:
            for ext in ("png", "svg"):
                self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(HERE), "categories", f"{tag.replace(' ', '-')}.{ext}")), tag)

    def test_banner(self):
        self.assertEqual(set(build_index.BANNER), {"title", "text"})
        self.assertEqual(build_index.BANNER["title"], "Welcome to Catalogue")


if __name__ == "__main__":
    unittest.main()
