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
     shot1.png ...    optional: screenshots
   ```

3. `listing.json`:

   ```json
   {
     "id": "hello",
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

   - `category`: `app`, `game`, `driver`, `library`, `codec`, `theme`, `tool` or `system`.
   - `tags`: one to five words from the vocabulary below. Catalogue builds its **Categories** page from them, so use
     the words exactly (the checker rejects any other). Say what the item *is* first, then what it is *for*.
   - `releases`: the tags you ask to be approved, or `"latest"` (the newest non-prerelease, picked up daily).
   - `compatibility.arch`: `arm` (phones), `x32` (PCs and virtual machines). Optional: `boards` (e.g. `["pinephone"]`),
     `min_core`, `legacy` (also runs on stock Symbian OS 9.x phones), `needs_platsec_hack` (installs only on a phone
     whose platform security is patched).
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

   **Icon.** Every listing should have an `icon.png` (square, 256 x 256 is ideal, at least 128 px) and, next to it, the
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
