# Adding a listing

1. Publish your item as a **GitHub release** in its own repository, with the installable file (a `.sis` / `.sisx`,
   or what `source.asset` matches) attached as a release asset.
2. Fork this repository and add a folder `listings/<id>/` (the id: lower case letters, digits, `-` and `.`):

   ```
   listings/hello/
     listing.json     required
     listing.md       optional: the long description (Markdown)
     icon.png         optional: square, at least 128 px
     shot1.png ...    optional: screenshots
   ```

3. `listing.json`:

   ```json
   {
     "id": "hello",
     "name": "Hello",
     "summary": "A one-line description",
     "category": "app",
     "license": "EPL-1.0",
     "homepage": "https://github.com/someone/hello",
     "source": {"type": "github", "repo": "someone/hello", "asset": "\\.sisx?$"},
     "releases": ["v1.0"],
     "compatibility": {"arch": ["arm", "x32"]},
     "icon": "icon.png",
     "screenshots": ["shot1.png"]
   }
   ```

   - `category`: `app`, `game`, `driver`, `library`, `codec`, `theme`, `tool` or `system`.
   - `releases`: the tags you ask to be approved, or `"latest"` (the newest non-prerelease, picked up daily).
   - `compatibility.arch`: `arm` (phones), `x32` (PCs and virtual machines). Optional: `boards` (e.g. `["pinephone"]`),
     `min_core`, `legacy` (also runs on stock Symbian OS 9.x phones), `needs_platsec_hack` (installs only on a phone
     whose platform security is patched).
   - `requires`: ids of listings that must be installed first.

4. Check it locally: `python3 tools/build_index.py --offline`.
5. Open a pull request that changes **only your folder**. Anything else (other listings, `index.json`, the schema,
   tools or workflows) gets the pull request closed automatically. A maintainer reviews it and merges by hand.

To update a listing (new approved tags, a new description), open a pull request on the same folder.
