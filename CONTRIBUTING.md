# Adding a listing

1. Publish your item as a **GitHub release** in its own repository, with the installable file (a `.sis` / `.sisx`,
   or what `source.asset` matches) attached as a release asset. The store text is yours too and lives in that
   repository, in a `catalogue/` folder (or the folder `source.text` names):

   ```
   catalogue/
     summary.txt      required: one line, up to 140 characters
     description.md   optional: the long description (Markdown)
   ```

   Catalogue takes them from your newest approved release (from the default branch when that release has none),
   so the text changes with your releases and never needs a pull request here.
2. Fork this repository and add a folder `listings/<id>/` (the id: lower case letters, digits, `-` and `.`):

   ```
   listings/hello/
     listing.json     required
     icon.png         optional: square, at least 128 px
     shot1.png ...    optional: screenshots (PNG, about 360 px wide: your own app running, nothing of anyone else's)
   ```

3. `listing.json`:

   ```json
   {
     "id": "hello",
     "group": "hello",
     "name": "Hello",
     "category": "app",
     "license": "EPL-1.0",
     "homepage": "https://github.com/someone/hello",
     "source": {"type": "github", "repo": "someone/hello", "asset": "\\.sisx?$"},
     "releases": ["v1.0"],
     "compatibility": {"arch": ["arm", "x32"]},
     "tags": ["library", "developer"],
     "icon": "icon.png",
     "screenshots": ["shot1.png"]
   }
   ```

   - `group` and `name`: one listing is one architecture's build of your app. Ship ARM and x32 packages as two listings
     (`hello-arm` and `hello-x32`, each with its own `asset` and `arch`) that share a `group` (the app's id on the web
     page, default: the listing's id) and the same `name`, with no "(PC)" or "(phones)" in it. The website shows one
     card per group, with a Download menu to pick the architecture; the phone shows the listing for its own
     architecture.
   - `category`: `app`, `game`, `driver`, `library`, `codec`, `theme`, `tool` or `system`.
   - `tags`: one to five words from the vocabulary below. Catalogue builds its **Categories** page from them, so use
     the words exactly (the checker rejects any other). Say what the item *is* first, then what it is *for*.
   - `releases`: the tags you ask to be approved, or `"latest"` (the newest non-prerelease, picked up daily).
   - `compatibility.arch`: `arm` (32-bit ARM: phones), `x32` (amd64 with 32-bit pointers: PCs and virtual machines);
     `aarch64` and `x64` are reserved for 64-bit userspace. Optional: `boards` (e.g. `["pinephone"]`),
     `min_core`, `legacy` (also runs on stock Symbian OS 9.x phones), `needs_platsec_hack` (installs only on a phone
     whose platform security is patched). `min_core` is the oldest core the item runs on, written as that core commit's
     UTC committer time, `YYYY.MM.DD.HHMMSS` (`TZ=UTC git log -1 --format=%cd --date=format-local:%Y.%m.%d.%H%M%S <commit>`
     in core). Every image states its own value as `core=` in `z:\resource\phorepoc\device.txt`, and Catalogue refuses
     an item whose `min_core` is newer ("Needs a newer system"). Set it when the package needs a core feature, for
     example the x32 loader's PC-relative imports (core fbeb597, `2026.11.10.165459`).
   - `requires`: ids of listings that must be installed first.

   **Tag vocabulary** (a fixed list; a new word is a change to `schema/listing.schema.json` by a maintainer):

   | Tag | Use it for |
   |---|---|
   | `browser engine` | a web engine the browser app can use (WebKit, NetSurf ...) |
   | `library` | code other programs link against (Qt, runtimes) |
   | `codec` | audio / video / image formats |
   | `driver` | hardware or device drivers |
   | `game` | games |
   | `theme` | looks: themes, fonts, wallpapers |
   | `tool` | small programs for a job (file tools, converters) |
   | `media` | music, video, photos |
   | `web` | browsing, the web, web services |
   | `graphics` | drawing, imaging, 3D |
   | `network` | connections, sync, VPN, file sharing |
   | `security` | keys, certificates, privacy |
   | `productivity` | notes, calendar, mail, documents |
   | `developer` | for people who write or port software |
   | `system` | changes how the system itself works |

   For example: WebKit and NetSurf are `["browser engine", "web"]`, Qt is `["library", "developer"]`, the codec pack
   is `["codec", "media"]`. Catalogue also shows each item under its `category`, so a listing without tags still appears
   in the matching group.

   **Icon.** Every listing should have an `icon.png` (square, 256 x 256 is ideal, at least 128 px). If you port a project
   that has an official logo, use that logo unmodified (scaled onto a transparent square), when its owner's terms allow
   it: put the credit and terms in `icon_credit` and add a row to [LOGOS.md](LOGOS.md). Otherwise add, next to the PNG, the
   `icon.svg` it came from. Draw icons in the [Etesian design language](https://language.etesian-design.com):
   a squircle tile (|x|^2.8 + |y|^2.8 = 1, not a rounded rectangle), one accent colour from the language's table,
   a glyph on a 24 x 24 grid drawn with a single 2 px round stroke, outline only, off-white, lit from above. Do not
   use another project's artwork or any vendor's icons; only your own work, under this repository's licence.
   `tools/make_icons.py` draws them: add a line to `ICONS` with a glyph from `tools/icongen.py` (add a glyph there
   if none fits) and an accent, run `python3 tools/make_icons.py`, and commit the two files.

4. Check it locally: `python3 tools/build_index.py --offline`.
5. Open a pull request that changes **only your folder**. Anything else (other listings, `index.json`, the schema,
   tools or workflows) gets the pull request closed automatically. A maintainer reviews it and merges by hand.

To update a listing (new approved tags, a new description), open a pull request on the same folder.
