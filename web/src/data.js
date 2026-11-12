// Copyright The Phorepoc Authors
// SPDX-License-Identifier: Apache-2.0
// The store's data: index.json (build time). Everything the pages show is derived here.
//
// index.json has one item per listing, and a listing is one architecture's build of an app (the phone installs one
// architecture and reads the items as they are). The site shows one card per app instead: the listings that share a
// "group" (default: the id) are one app, with one package per architecture.
import index from '@index'

export const SITE = 'Phorepoc Catalogue'
export const generated = index.generated
export const banner = { title: SITE, text: 'Apps, codecs, engines and tools for Phorepoc, on ARM and x32. All open source.' }

// architectures, in the order the download menu offers them (64-bit userspace comes later)
export const ARCHES = ['arm', 'x32', 'aarch64', 'x64']
const ARCH_INFO = {
  arm: { label: 'ARM', note: 'ARM (32-bit)' },
  x32: { label: 'x32', note: 'x32 (amd64, 32-bit pointers)' },
  aarch64: { label: 'AArch64', note: 'AArch64 (64-bit ARM)' },
  x64: { label: 'x64', note: 'x64 (amd64, 64-bit)' },
}
export const archLabelOf = (a) => (ARCH_INFO[a] ? ARCH_INFO[a].label : a)
export const archNoteOf = (a) => (ARCH_INFO[a] ? ARCH_INFO[a].note : '')

const time = (r) => Date.parse(r.published) || 0
const groupOf = (item) => item.group || item.id
const archOf = (item) => item.compatibility.arch[0]
const all = index.items || []

function groupOfId(id) {
  const i = all.find((x) => x.id === id)
  return i ? groupOf(i) : id
}

function makeApps() {
  const by = new Map()
  for (const i of all) {
    if (!by.has(groupOf(i))) by.set(groupOf(i), [])
    by.get(groupOf(i)).push(i)
  }
  const apps = []
  for (const [id, builds] of by) {
    builds.sort((a, b) => ARCHES.indexOf(archOf(a)) - ARCHES.indexOf(archOf(b)))
    const first = builds.find((b) => b.description) || builds[0]
    // each architecture's listing carries its own copy of a screenshot: one per file name
    const seen = new Set()
    const screenshots = builds.flatMap((b) => b.screenshot_urls || []).filter((s) => {
      const k = s.split('/').pop()
      return seen.has(k) ? false : seen.add(k)
    })
    const packages = builds.map((b) => {
      const r = [...(b.resolved || [])].sort((x, y) => time(y) - time(x))[0]
      return r && { arch: archOf(b), listing: b.id, needsPlatsecHack: !!b.compatibility.needs_platsec_hack, ...r }
    }).filter(Boolean)
    apps.push({
      id, name: first.name, summary: first.summary, description: first.description, category: first.category,
      tags: first.tags || [], license: first.license, homepage: first.homepage, authors: first.authors,
      source: first.source, icon_url: first.icon_url, icon_credit: first.icon_credit, screenshots,
      legacy: builds.some((b) => b.compatibility.legacy),
      featured: builds.some((b) => b.featured === true),
      requires: [...new Set(builds.flatMap((b) => b.requires || []).map(groupOfId))],
      arches: builds.map(archOf),
      packages,
      published: Math.max(0, ...packages.map(time)),
    })
  }
  return apps.sort((a, b) => b.published - a.published || a.name.localeCompare(b.name))
}

export const apps = makeApps()
export const NEW_COUNT = 8
export const newApps = apps.slice(0, NEW_COUNT)
export const self = apps.find((a) => a.id === 'catalogue')

// featured on the home page: the apps whose listings say "featured": true (newest first); none = the newest with screenshots
export const featured = (() => {
  const f = apps.filter((a) => a.featured)
  return f.length ? f : apps.filter((a) => a.screenshots.length).slice(0, 6)
})()

export const slug = (tag) => tag.replace(/ /g, '-')
export const inCategory = (tag) => apps.filter((i) => i.tags.includes(tag) || i.category === tag)
// the index counts listings (one per architecture); the site counts apps
export const categories = (index.categories || []).map((c) => ({ ...c, count: inCategory(c.tag).length })).filter((c) => c.count)
export const categoryBySlug = (s) => categories.find((c) => slug(c.tag) === s)
// an app by its group, or by one of its listings' ids, so the older /app/<listing id>/ addresses keep working
export const itemById = (id) => apps.find((a) => a.id === id) || apps.find((a) => a.packages.some((p) => p.listing === id))
export const oldIds = () => all.map((i) => i.id).filter((id) => !apps.some((a) => a.id === id))

export function formatSize(n) {
  if (n >= 1048576) return (n / 1048576).toFixed(1) + ' MB'
  if (n >= 1024) return Math.round(n / 1024) + ' KB'
  return n + ' B'
}

export const archLabel = (app) => app.arches.map(archLabelOf).join(', ')

export function search(q) {
  const words = q.toLowerCase().split(/\s+/).filter(Boolean)
  if (!words.length) return []
  return apps.filter((i) => {
    const hay = [i.name, i.summary, i.id, ...i.tags, i.category, i.description || '', ...i.arches].join(' ').toLowerCase()
    return words.every((w) => hay.includes(w))
  })
}
