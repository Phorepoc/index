// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { renderToString } from 'vue/server-renderer'
import { createApp } from './app.js'
import { prerenderPaths } from './router.js'
import { itemById, categoryBySlug, banner } from './data.js'
import { pageMeta } from './meta.js'

export { prerenderPaths }

export async function render(path) {
  const { app, router } = createApp(true, { req: { headers: {} }, res: {}, _meta: {}, onRendered() {} })
  router.push(path)
  await router.isReady()
  return { html: await renderToString(app), meta: pageMeta(router.currentRoute.value, { itemById, categoryBySlug, banner }) }
}
