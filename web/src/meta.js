// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
// <title> and description of a route (prerendered into the HTML; the client updates the title on navigation)
const SITE = 'Phorepoc Catalogue'
export function pageMeta(route, { itemById, categoryBySlug, banner }) {
  const p = route.params
  if (route.path.startsWith('/app/')) {
    const i = itemById(p.id)
    if (i) return { title: `${i.name} - ${SITE}`, description: i.summary }
  }
  if (route.path.startsWith('/category/')) {
    const c = categoryBySlug(p.slug)
    if (c) return { title: `${c.name} - ${SITE}`, description: `${c.name}: ${c.count} item(s) in ${SITE}.` }
  }
  if (route.path.startsWith('/apps/')) return { title: `All apps - ${SITE}`, description: `Every app in ${SITE}, newest first.` }
  if (route.path.startsWith('/search/')) return { title: `Search - ${SITE}`, description: 'Search the catalogue.' }
  return { title: SITE, description: banner.text }
}
