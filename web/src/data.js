// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
// The store's data: index.json (build time). Everything the pages show is derived here.
import index from '@index'

export const items = [...index.items].sort((a, b) => newest(b) - newest(a) || a.name.localeCompare(b.name))
export const categories = index.categories || []
export const banner = index.banner || { title: 'Welcome to Catalogue', text: '' }
export const generated = index.generated

function newest(item) {
  return Math.max(0, ...(item.resolved || []).map((r) => Date.parse(r.published) || 0))
}

export const slug = (tag) => tag.replace(/ /g, '-')
export const categoryBySlug = (s) => categories.find((c) => slug(c.tag) === s)
export const itemById = (id) => items.find((i) => i.id === id)
export const inCategory = (tag) => items.filter((i) => (i.tags || []).includes(tag) || i.category === tag)

export function formatSize(n) {
  if (n >= 1048576) return (n / 1048576).toFixed(1) + ' MB'
  if (n >= 1024) return Math.round(n / 1024) + ' KB'
  return n + ' B'
}

export const archLabel = (item) => (item.compatibility?.arch || []).map((a) => a.toUpperCase()).join(', ')

export function search(q) {
  const words = q.toLowerCase().split(/\s+/).filter(Boolean)
  if (!words.length) return []
  return items.filter((i) => {
    const hay = [i.name, i.summary, i.id, ...(i.tags || []), i.category, i.description || ''].join(' ').toLowerCase()
    return words.every((w) => hay.includes(w))
  })
}
