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
    "id": "hello", "name": "Hello", "summary": "Says hello", "category": "app", "license": "EPL-1.0",
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


if __name__ == "__main__":
    unittest.main()
