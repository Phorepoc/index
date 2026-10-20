# Copyright The Phorepoc Authors
# SPDX-License-Identifier: Apache-2.0

"""build_index -- validate every listing and write the generated index (index.json) the download app reads.

    python3 tools/build_index.py [--out index.json] [--offline]

For each listings/<id>/listing.json: validate it against schema/listing.schema.json (and the folder rules: the id is
the folder's name, icon and screenshots exist), then resolve its approved releases on GitHub -- every release's
installable asset (the file name matching `source.asset`), its download URL, size and SHA-256 (downloaded once and
hashed here, so the app can check what it fetched). --offline skips the GitHub part (validation only: what a pull
request check runs). GITHUB_TOKEN, when set, raises the API rate limit.

Output (sorted by id, stable):
  {"format": 1, "generated": "<UTC time>", "items": [{<the listing>, "description": ..., "icon_url": ...,
   "screenshot_urls": [...], "resolved": [{"tag", "published", "asset", "url", "size", "sha256"}, ...]}, ...]}
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTINGS = os.path.join(ROOT, "listings")
SCHEMA = os.path.join(ROOT, "schema", "listing.schema.json")
BASE = os.environ.get("INDEX_BASE", "https://phorepoc.github.io/index")   # where publish.yml serves the site


class Invalid(Exception):
    pass


def check(value, schema: dict, where: str) -> None:
    """the subset of JSON Schema the listing schema uses (no third-party module needed in CI or on a laptop)"""
    if "oneOf" in schema:
        errors = []
        for alt in schema["oneOf"]:
            try:
                check(value, alt, where)
                return
            except Invalid as e:
                errors.append(str(e))
        raise Invalid(f"{where}: matches none of the allowed forms ({'; '.join(errors)})")
    if "const" in schema and value != schema["const"]:
        raise Invalid(f"{where}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise Invalid(f"{where}: {value!r} is not one of {schema['enum']}")
    t = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool}
    if t and not isinstance(value, types[t]):
        raise Invalid(f"{where}: must be a {t}")
    if t == "string":
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", 1 << 30):
            raise Invalid(f"{where}: length out of range")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            raise Invalid(f"{where}: {value!r} does not match {schema['pattern']}")
        if schema.get("format") == "uri" and not re.match(r"^https?://", value):
            raise Invalid(f"{where}: not an http(s) URL")
    if t == "array":
        if len(value) < schema.get("minItems", 0):
            raise Invalid(f"{where}: needs at least {schema['minItems']} item(s)")
        for i, item in enumerate(value):
            check(item, schema.get("items", {}), f"{where}[{i}]")
    if t == "object":
        for key in schema.get("required", []):
            if key not in value:
                raise Invalid(f"{where}: missing {key!r}")
        props = schema.get("properties", {})
        for key, item in value.items():
            if key not in props:
                if schema.get("additionalProperties") is False:
                    raise Invalid(f"{where}: unknown field {key!r}")
                continue
            check(item, props[key], f"{where}.{key}")


def load_listing(lid: str, schema: dict) -> dict:
    folder = os.path.join(LISTINGS, lid)
    path = os.path.join(folder, "listing.json")
    if not os.path.isfile(path):
        raise Invalid(f"{lid}: no listing.json")
    try:
        listing = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        raise Invalid(f"{lid}/listing.json: not JSON ({e})")
    check(listing, schema, lid)
    if listing["id"] != lid:
        raise Invalid(f"{lid}: id {listing['id']!r} must be the folder's name")
    for f in ([listing["icon"]] if "icon" in listing else []) + listing.get("screenshots", []):
        if "/" in f or "\\" in f or not os.path.isfile(os.path.join(folder, f)):
            raise Invalid(f"{lid}: {f!r} is not a file in the listing folder")
    if "description" not in listing and os.path.isfile(os.path.join(folder, "listing.md")):
        listing["description"] = open(os.path.join(folder, "listing.md"), encoding="utf-8").read()
    return listing


def github(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "phorepoc-index"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r) if "api.github.com" in url else r.read()


def resolve(listing: dict) -> list:
    repo = listing["source"]["repo"]
    pattern = re.compile(listing["source"].get("asset", r"\.sisx?$"))
    if listing["releases"] == "latest":
        rels = [github(f"https://api.github.com/repos/{repo}/releases/latest")]
    else:
        rels = [github(f"https://api.github.com/repos/{repo}/releases/tags/{t}") for t in listing["releases"]]
    out = []
    for rel in rels:
        assets = [a for a in rel.get("assets", []) if pattern.search(a["name"])]
        if not assets:
            raise Invalid(f"{listing['id']}: release {rel.get('tag_name')} has no asset matching {pattern.pattern}")
        for a in assets:
            data = github(a["browser_download_url"])
            out.append({"tag": rel["tag_name"], "published": rel.get("published_at"), "asset": a["name"],
                        "url": a["browser_download_url"], "size": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "index.json"))
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    items, errors = [], []
    for lid in sorted(os.listdir(LISTINGS)) if os.path.isdir(LISTINGS) else []:
        if not os.path.isdir(os.path.join(LISTINGS, lid)):
            continue
        try:
            item = load_listing(lid, schema)
            url = lambda f: f"{BASE}/listings/{lid}/{f}"   # noqa: E731
            if "icon" in item:
                item["icon_url"] = url(item["icon"])
            item["screenshot_urls"] = [url(f) for f in item.get("screenshots", [])]
            if not a.offline:
                try:
                    item["resolved"] = resolve(item)
                except (Invalid, OSError) as e:
                    # one listing whose releases cannot be resolved (none yet, a deleted tag) does not take the
                    # whole index down: it is left out until it resolves again
                    print("WARNING", f"{lid}: left out: {e}")
                    continue
            items.append(item)
        except Invalid as e:
            errors.append(str(e))
        except OSError as e:
            errors.append(f"{lid}: {e}")
    for e in errors:
        print("ERROR", e)
    if errors:
        return 1
    if not a.offline:
        doc = {"format": 1, "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "items": items}
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    print(f"build_index: {len(items)} listing(s) valid" + ("" if a.offline else f", written to {a.out}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
