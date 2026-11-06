<script setup>
import { computed } from 'vue'
import { QBtn } from 'quasar'
import MarkdownIt from 'markdown-it'
import { itemById, formatSize, archLabel, categories, slug } from '../data.js'
const props = defineProps({ id: String })
const md = new MarkdownIt({ html: false, linkify: true })
const item = computed(() => itemById(props.id))
const html = computed(() => (item.value && item.value.description ? md.render(item.value.description) : ''))
const tags = computed(() => ((item.value && item.value.tags) || []).map((t) => categories.find((c) => c.tag === t)).filter(Boolean))
const downloads = computed(() => (item.value && item.value.resolved) || [])
const date = (s) => (s ? s.slice(0, 10) : '')
</script>

<template>
  <nav class="crumbs" aria-label="Breadcrumb"><router-link to="/">Catalogue</router-link> / <span>{{ item ? item.name : 'App' }}</span></nav>
  <article v-if="item" class="app-page">
    <header class="page-head">
      <img class="icon big" :src="item.icon_url" alt="" width="96" height="96">
      <div>
        <h1>{{ item.name }}</h1>
        <p class="summary">{{ item.summary }}</p>
        <ul class="chips" aria-label="Categories">
          <li v-for="c in tags" :key="c.tag"><router-link :to="`/category/${slug(c.tag)}/`" class="chip">{{ c.name }}</router-link></li>
        </ul>
      </div>
    </header>

    <section class="panel" aria-labelledby="dl">
      <h2 id="dl">Download</h2>
      <ul v-if="downloads.length" class="downloads">
        <li v-for="d in downloads" :key="d.url">
          <q-btn unelevated color="primary" no-caps :href="d.url" :label="`Download ${d.asset}`" :aria-label="`Download ${d.asset}, ${formatSize(d.size)}`" />
          <div class="dl-meta">
            <span>{{ archLabel(item) }} &middot; {{ formatSize(d.size) }} &middot; {{ d.tag }}<template v-if="d.published"> &middot; {{ date(d.published) }}</template></span>
            <span class="sha">SHA-256 <code>{{ d.sha256 }}</code></span>
          </div>
        </li>
      </ul>
      <p v-else class="muted">No approved release is available yet.</p>
      <h3>How to install</h3>
      <p>Copy the <code>.sis</code> file to the phone and open it, or install this app from Catalogue on the phone.</p>
    </section>

    <section v-if="html" class="panel prose" aria-labelledby="about">
      <h2 id="about">About</h2>
      <div v-html="html" />
    </section>

    <section class="panel" aria-labelledby="det">
      <h2 id="det">Details</h2>
      <dl class="details">
        <dt>Licence</dt><dd>{{ item.license }}</dd>
        <dt>Architecture</dt><dd>{{ archLabel(item) }}</dd>
        <template v-if="item.compatibility && item.compatibility.legacy"><dt>Compatibility</dt><dd>Also runs on stock Symbian OS 9.x phones</dd></template>
        <template v-if="item.requires && item.requires.length"><dt>Needs first</dt><dd><template v-for="(r, n) in item.requires" :key="r"><router-link :to="`/app/${r}/`">{{ r }}</router-link><template v-if="n < item.requires.length - 1">, </template></template></dd></template>
        <template v-if="item.authors && item.authors.length"><dt>Authors</dt><dd>{{ item.authors.join(', ') }}</dd></template>
        <dt>Source</dt><dd><a :href="`https://github.com/${item.source.repo}`">github.com/{{ item.source.repo }}</a></dd>
        <template v-if="item.homepage"><dt>Homepage</dt><dd><a :href="item.homepage">{{ item.homepage }}</a></dd></template>
      </dl>
    </section>

    <section v-if="item.screenshot_urls && item.screenshot_urls.length" class="panel" aria-labelledby="shots">
      <h2 id="shots">Screenshots</h2>
      <div class="shots"><img v-for="s in item.screenshot_urls" :key="s" :src="s" alt="Screenshot" loading="lazy"></div>
    </section>
  </article>
  <p v-else>No such app. <router-link to="/">Back to the catalogue</router-link></p>
</template>
