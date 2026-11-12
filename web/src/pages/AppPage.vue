<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import { itemById, formatSize, archLabel, archLabelOf, archNoteOf, categories, slug } from '../data.js'
import DownloadMenu from '../components/DownloadMenu.vue'
const props = defineProps({ id: String })
const md = new MarkdownIt({ html: false, linkify: true })
const item = computed(() => itemById(props.id))
const html = computed(() => (item.value && item.value.description ? md.render(item.value.description) : ''))
const tags = computed(() => ((item.value && item.value.tags) || []).map((t) => categories.find((c) => c.tag === t)).filter(Boolean))
const downloads = computed(() => (item.value && item.value.packages) || [])
const hack = computed(() => downloads.value.some((d) => d.needsPlatsecHack))
const date = (s) => (s ? s.slice(0, 10) : '')
</script>

<template>
  <nav class="crumbs" aria-label="Breadcrumb"><router-link to="/">Phorepoc Catalogue</router-link> / <span>{{ item ? item.name : 'App' }}</span></nav>
  <article v-if="item" class="app-page">
    <header class="page-head">
      <img class="icon big" :src="item.icon_url" alt="" width="96" height="96">
      <div>
        <h1>{{ item.name }}</h1>
        <p class="summary">{{ item.summary }}</p>
        <DownloadMenu v-if="downloads.length" :app="item" class="head-dl" />
        <ul class="chips" aria-label="Categories">
          <li v-for="c in tags" :key="c.tag"><router-link :to="`/category/${slug(c.tag)}/`" class="chip">{{ c.name }}</router-link></li>
        </ul>
      </div>
    </header>

    <section class="panel" aria-labelledby="dl">
      <h2 id="dl">Files</h2>
      <ul v-if="downloads.length" class="downloads">
        <li v-for="d in downloads" :key="d.url">
          <a class="dl-file" :href="d.url"><strong>{{ archLabelOf(d.arch) }}</strong> {{ d.asset }}</a>
          <div class="dl-meta">
            <span>{{ archNoteOf(d.arch) }} &middot; {{ formatSize(d.size) }} &middot; {{ d.tag }}<template v-if="d.published"> &middot; {{ date(d.published) }}</template></span>
            <span class="sha">SHA-256 <code>{{ d.sha256 }}</code></span>
          </div>
        </li>
      </ul>
      <p v-else class="muted">No approved release is available yet.</p>
      <h3>How to install</h3>
      <p>Copy the <code>.sis</code> file to the device and open it, or install this app from Catalogue on the device.</p>
    </section>

    <section v-if="item.screenshots.length" class="panel" aria-labelledby="shots">
      <h2 id="shots">Screenshots</h2>
      <div class="shots"><img v-for="(s, n) in item.screenshots" :key="s" :src="s" :alt="`${item.name}, screenshot ${n + 1}`" loading="lazy"></div>
    </section>

    <section v-if="html.trim()" class="panel prose" aria-labelledby="about">
      <h2 id="about">About</h2>
      <div class="desc" v-html="html" />
    </section>

    <section class="panel" aria-labelledby="det">
      <h2 id="det">Details</h2>
      <dl class="details">
        <dt>Licence</dt><dd>{{ item.license }}</dd>
        <dt>Architecture</dt><dd>{{ archLabel(item) }}</dd>
        <template v-if="item.legacy"><dt>Compatibility</dt><dd>The ARM package also runs on older Symbian^3 phones<template v-if="hack">, on one whose installation check is lifted (or with the package signed)</template></dd></template>
        <template v-if="item.requires && item.requires.length"><dt>Needs first</dt><dd><template v-for="(r, n) in item.requires" :key="r"><router-link :to="`/app/${r}/`">{{ r }}</router-link><template v-if="n < item.requires.length - 1">, </template></template></dd></template>
        <template v-if="item.authors && item.authors.length"><dt>Authors</dt><dd>{{ item.authors.join(', ') }}</dd></template>
        <template v-if="item.icon_credit"><dt>Logo</dt><dd>{{ item.icon_credit }}</dd></template>
        <dt>Source</dt><dd><a :href="`https://github.com/${item.source.repo}`">github.com/{{ item.source.repo }}</a></dd>
        <template v-if="item.homepage"><dt>Homepage</dt><dd><a :href="item.homepage">{{ item.homepage }}</a></dd></template>
      </dl>
    </section>

    
  </article>
  <p v-else>No such app. <router-link to="/">Back to the catalogue</router-link></p>
</template>
