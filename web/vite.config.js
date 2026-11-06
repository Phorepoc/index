// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar } from '@quasar/vite-plugin'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'

// The store's data is the generated index.json (INDEX_JSON, default ../site/index.json: where publish.yml writes it), read at
// build time and bundled, so every page is prerendered from it and the search needs no request.
const indexJson = resolve(process.env.INDEX_JSON || fileURLToPath(new URL('../site/index.json', import.meta.url)))

export default defineConfig(({ isSsrBuild }) => ({
  base: '/index/',
  plugins: [vue(), quasar({ runMode: isSsrBuild ? 'ssr-server' : 'ssr-client' })],
  resolve: { alias: { '@index': indexJson } },
  ssr: { noExternal: ['quasar'] },
  build: { outDir: 'dist', emptyOutDir: true },
}))
