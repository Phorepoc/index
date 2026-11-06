// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { renderToString } from 'vue/server-renderer'
import { createApp } from './app.js'
import { prerenderPaths } from './router.js'
import { itemById, categoryBySlug, banner } from './data.js'
import { pageMeta } from './meta.js'

export { prerenderPaths }

// Quasar fills ssrContext._meta while rendering (body classes, the dark-mode marker, the brand colours as a <style>) and
// finishes it in its onRendered hooks; the page template takes all of it
export async function render(path) {
  const rendered = []
  const ssrContext = { req: { headers: {} }, res: {}, onRendered(fn) { rendered.push(fn) } }
  const { app, router } = createApp(true, ssrContext)
  router.push(path)
  await router.isReady()
  const html = await renderToString(app, ssrContext)
  for (const fn of rendered) fn()
  return { html, quasar: ssrContext._meta, meta: pageMeta(router.currentRoute.value, { itemById, categoryBySlug, banner }) }
}
