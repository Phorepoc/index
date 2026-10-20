# Copyright The Phorepoc Authors
# SPDX-License-Identifier: Apache-2.0

"""check_pr -- the pull request gate: a contributor's PR may only add or change files inside ONE listing folder
(listings/<id>/...). Anything else -- the generated index.json, the schema, the tools, the workflows, another
listing -- needs a maintainer. Run by .github/workflows/pr.yml with the PR's changed files on stdin (one per line).

    git diff --name-only <base>...<head> | python3 tools/check_pr.py [--maintainer]

--maintainer (the workflow passes it when the author has write access to this repository): everything is allowed.
Exit 1 with the reasons when the PR is out of bounds.
"""
from __future__ import annotations

import re
import sys

LISTING_FILE = re.compile(r"^listings/([a-z0-9][a-z0-9.-]{1,62})/[^/]+$")


def main() -> int:
    files = [l.strip() for l in sys.stdin if l.strip()]
    if "--maintainer" in sys.argv:
        print(f"check_pr: maintainer PR, {len(files)} file(s), no restrictions")
        return 0
    folders, outside = set(), []
    for f in files:
        m = LISTING_FILE.match(f)
        if m:
            folders.add(m.group(1))
        else:
            outside.append(f)
    errors = []
    if outside:
        errors.append("files outside a listing folder (only maintainers change these): " + ", ".join(outside))
    if len(folders) > 1:
        errors.append("one listing per pull request, this one touches: " + ", ".join(sorted(folders)))
    if not files:
        errors.append("no changed files")
    for e in errors:
        print("REJECT", e)
    if errors:
        return 1
    print(f"check_pr: OK, listing {next(iter(folders))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
