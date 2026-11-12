// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { createRouter, createMemoryHistory, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Category from './pages/Category.vue'
import App from './pages/AppPage.vue'
import Search from './pages/Search.vue'
import AllApps from './pages/AllApps.vue'
import { categories, apps, oldIds, slug } from './data.js'

export const routes = [
  { path: '/', component: Home },
  { path: '/category/:slug/', component: Category, props: true },
  { path: '/app/:id/', component: App, props: true },
  { path: '/search/', component: Search },
  { path: '/apps/', component: AllApps },
  { path: '/:rest(.*)*', component: Home },
]

// every route that gets a prerendered page
export const prerenderPaths = () => [
  '/', '/search/', '/apps/',
  ...categories.map((c) => `/category/${slug(c.tag)}/`),
  ...apps.map((i) => `/app/${i.id}/`),
  // the older one-listing-per-architecture addresses: the app's page
  ...oldIds().map((id) => `/app/${id}/`),
]

export const makeRouter = (server) =>
  createRouter({
    history: server ? createMemoryHistory('/index/') : createWebHistory('/index/'),
    routes,
    scrollBehavior: () => ({ top: 0 }),
  })
