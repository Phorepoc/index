// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { createApp } from './app.js'

const { app, router } = createApp(false)
router.isReady().then(() => {
  app.mount('#app', true)
  app.config.globalProperties.$q.onSSRHydrated()   // Quasar's prerendered state (dark 'auto', platform classes) resolves now
})
