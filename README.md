# index

This is the list of apps, games, drivers and codecs you can install from the Catalogue, Phorepoc's software store. Nothing is
hosted here. Each app lives in its own repository and publishes its own releases. This list just says which repository,
which releases are approved, and which devices they're for.

The Catalogue reads the published list at **https://phorepoc.github.io/index/index.json**, which is rebuilt every time
something is merged, and once a day.

## How it works

Every app has a folder in `listings/`, with a `listing.json` that follows
[the schema](schema/listing.schema.json). It can also have a longer description in `listing.md`, an icon and
screenshots. The listing names the app's repository and the releases we've approved, either specific tags or simply
`"latest"`.

When the list is published, a workflow looks up each approved release on GitHub. It finds the file to install and
records its address, size and SHA-256. A release it can't find is left out until it can.

On the phone, the Catalogue only shows what fits the device, downloads the file and checks its SHA-256 before installing.
People can also add other lists and single repositories next to this one. This is just the default.

## Adding your app

Open a pull request that adds or changes **one** folder in `listings/`. [CONTRIBUTING.md](CONTRIBUTING.md) walks you
through it. Pull requests that touch anything else are closed automatically, and a maintainer reviews each listing by
hand before merging.

## Working on the index itself

`tools/build_index.py` checks the listings and builds `index.json`, and `--offline` only does the checks.
`tools/check_pr.py` is what enforces the one-folder rule. The tests run with
`python3 -m unittest discover -s tests`.

## License

Apache-2.0. Listings are contributed under the same license, and the apps they point to keep their own.

Add your name to `AUTHORS` in your first pull request.
