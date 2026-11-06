// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { createSSRApp } from 'vue'
import { Quasar } from 'quasar'
import { etesianQuasarOptions, EtesianQuasar } from '@etesian-design/quasar'
import 'quasar/dist/quasar.css'
import '@etesian-design/tokens/styles/tokens.css'
import '@etesian-design/tokens/styles/base.css'
import './css/fonts.css'
import '@etesian-design/quasar/theme.css'
import './css/store.css'
import Root from './Root.vue'
import { makeRouter } from './router.js'

export function createApp(server, ssrContext) {
  const app = createSSRApp(Root)
  const router = makeRouter(server)
  app.use(Quasar, etesianQuasarOptions(), ssrContext).use(EtesianQuasar).use(router)
  return { app, router }
}
