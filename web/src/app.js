// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { createSSRApp } from 'vue'
import { Quasar } from 'quasar'
import 'quasar/dist/quasar.css'
import './css/etesian/tokens.css'
import './css/etesian/base.css'
import './css/fonts.css'
import './css/etesian/quasar-theme.css'
import './css/store.css'
import Root from './Root.vue'
import { makeRouter } from './router.js'

export function createApp(server, ssrContext) {
  const app = createSSRApp(Root)
  const router = makeRouter(server)
  app.use(Quasar, {}, ssrContext).use(router)
  return { app, router }
}
