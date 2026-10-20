# index

Phorepoc's software index: the list of apps, games, drivers, codecs and libraries the Phorepoc download app offers,
and which of their releases are approved. Items stay in their own repositories and publish their own releases; this
repository only says **which repository, which releases, for which devices**.

The published index: **https://phorepoc.github.io/index/index.json** (rebuilt on every merge and daily).

## How it works

- Each item has a folder `listings/<id>/` with a `listing.json` (format: [`schema/listing.schema.json`](schema/listing.schema.json)),
  optionally `listing.md` (the long description), an icon and screenshots.
- A listing names its source repository and the approved releases: explicit tags, or `"latest"`.
- The `publish` workflow resolves every approved release on GitHub (the installable asset, its download URL, size and
  SHA-256) and publishes `index.json` with the icons and screenshots on GitHub Pages. A listing whose release cannot be
  resolved is left out until it can.
- The download app reads `index.json`, shows only what fits the device (architecture, board, core version), downloads
  the asset and checks its SHA-256.

The app is open: users can add other indexes and single repositories next to this one. This index is the curated
default.

## Adding or updating a listing

Open a pull request that touches **one** `listings/<id>/` folder: see [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests
that change anything else are closed automatically (only maintainers change the schema, the tools, the workflows and
the generated index). A maintainer reviews and merges by hand.

## Layout

| path | what |
|---|---|
| `listings/<id>/` | one item: `listing.json`, `listing.md`, icon, screenshots |
| `schema/listing.schema.json` | the listing format |
| `tools/build_index.py` | validates the listings and builds `index.json` (`--offline`: validation only) |
| `tools/check_pr.py` | the pull request gate |
| `.github/workflows/` | `pr-gate` (one folder per PR), `validate` (the listings), `publish` (index.json on Pages) |
| `tests/` | `python3 -m unittest discover -s tests` |

## Licence

Apache-2.0 (see `LICENSE`), copyright The Phorepoc Authors (`AUTHORS`, `NOTICE`). Listings are contributed under the
same licence; the items they point to keep their own licences.

Contributions are welcome under the same terms: add yourself to `AUTHORS`.
