// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
import { createRouter, createMemoryHistory, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Category from './pages/Category.vue'
import App from './pages/AppPage.vue'
import Search from './pages/Search.vue'
import { categories, items, slug } from './data.js'

export const routes = [
  { path: '/', component: Home },
  { path: '/category/:slug/', component: Category, props: true },
  { path: '/app/:id/', component: App, props: true },
  { path: '/search/', component: Search },
  { path: '/:rest(.*)*', component: Home },
]

// every route that gets a prerendered page
export const prerenderPaths = () => [
  '/', '/search/',
  ...categories.map((c) => `/category/${slug(c.tag)}/`),
  ...items.map((i) => `/app/${i.id}/`),
]

export const makeRouter = (server) =>
  createRouter({
    history: server ? createMemoryHistory('/index/') : createWebHistory('/index/'),
    routes,
    scrollBehavior: () => ({ top: 0 }),
  })
