<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { QInput } from 'quasar'
import { itemById, categoryBySlug, banner } from './data.js'
import { pageMeta } from './meta.js'

const base = import.meta.env.BASE_URL
const route = useRoute()
const router = useRouter()
const q = ref(String(route.query.q || ''))

// the search box lives in the header: typing shows the results page, clearing it goes back
watch(q, (v) => {
  if (v && v.trim()) router.replace({ path: '/search/', query: { q: v } })
  else if (route.path === '/search/') router.replace({ path: '/' })
})
watch(() => route.fullPath, () => {
  if (route.path !== '/search/' && q.value) q.value = ''
  if (typeof document !== 'undefined') document.title = pageMeta(route, { itemById, categoryBySlug, banner }).title
})
</script>

<template>
  <a class="skip" href="#main">Skip to content</a>
  <header class="bar">
    <div class="bar-in">
      <router-link to="/" class="brand" aria-label="Catalogue home">
        <img :src="`${base}favicon.png`" alt="" width="32" height="32">
        <span>Catalogue</span>
      </router-link>
      <form class="search" role="search" @submit.prevent>
        <q-input v-model="q" class="hd-theme-light" :dark="false" type="search" dense outlined label="Search" aria-label="Search the catalogue" clearable />
      </form>
    </div>
  </header>
  <main id="main">
    <router-view />
  </main>
  <footer class="foot">
    <p>Catalogue is the app source for Phorepoc phones. Everything listed is open source, and each item links to its source.</p>
    <p><a href="https://github.com/Phorepoc/index">Add or update a listing</a> &middot; <a href="/index/index.json">index.json</a></p>
  </footer>
</template>
