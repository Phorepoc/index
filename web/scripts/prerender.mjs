// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
// Prerender: every route (home, search, each category, each app) is rendered with the SSR build and written as its own
// index.html next to the client bundle, so the pages work without JavaScript and load fast; the client then hydrates.
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const dist = join(root, 'dist')
const template = readFileSync(join(dist, 'index.html'), 'utf8')
const mod = await import(pathToFileURL(join(root, 'dist-ssr', 'entry-server.js')).href)

const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;')
let n = 0
for (const path of mod.prerenderPaths()) {
  const { html, meta } = await mod.render(path)
  const page = template
    .replace('<!--app-title-->', esc(meta.title))
    .replace('<!--app-description-->', esc(meta.description || ''))
    .replace('<!--app-html-->', html)
  const out = join(dist, path.replace(/^\//, ''), 'index.html')
  mkdirSync(dirname(out), { recursive: true })
  writeFileSync(out, page)
  if (path === '/') writeFileSync(join(dist, '404.html'), page)   // unknown address: the client router shows the right page or the home
  n++
}
rmSync(join(root, 'dist-ssr'), { recursive: true, force: true })
console.log(`prerender: ${n} pages`)
