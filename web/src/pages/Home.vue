<script setup>
import { ref } from 'vue'
import { banner, categories, newApps, apps, featured, self, slug, NEW_COUNT, archLabelOf } from '../data.js'
import AppCard from '../components/AppCard.vue'
import DownloadMenu from '../components/DownloadMenu.vue'
const base = import.meta.env.BASE_URL
// the featured carousel: a scroll-snap strip (swipe on a phone); the arrows page it by one card width
const strip = ref(null)
function page(dir) {
  const el = strip.value
  if (!el) return
  const card = el.querySelector('li')
  el.scrollBy({ left: dir * (card ? card.offsetWidth + 16 : el.clientWidth), behavior: 'smooth' })
}
</script>

<template>
  <section class="hero">
    <img class="hero-logo" :src="`${base}favicon.png`" alt="" width="96" height="96">
    <h1>{{ banner.title }}</h1>
    <p>{{ banner.text }}</p>
    <div v-if="self" class="hero-actions">
      <DownloadMenu :app="self" label="Download Catalogue" />
      <router-link :to="`/app/${self.id}/`" class="btn-outline">About the app</router-link>
    </div>
    <p v-if="self" class="hero-note">Catalogue is built into Phorepoc. The SIS file is for systems built without it, and the
      ARM one also installs on older Symbian^3 systems. Catalogue keeps itself up to date from this list.</p>
  </section>

  <section v-if="featured.length" class="featured" aria-labelledby="feat">
    <div class="sec-head">
      <h2 id="feat">Featured</h2>
      <div class="arrows">
        <button type="button" class="arrow" aria-label="Previous" @click="page(-1)">&lsaquo;</button>
        <button type="button" class="arrow" aria-label="Next" @click="page(1)">&rsaquo;</button>
      </div>
    </div>
    <ul ref="strip" class="carousel">
      <li v-for="a in featured" :key="a.id">
        <router-link :to="`/app/${a.id}/`" class="card feat-card">
          <span class="feat-banner">
            <img v-if="a.screenshots.length" class="feat-shot" :src="a.screenshots[0]" alt="" loading="lazy">
            <span class="feat-title">
              <img class="icon" :src="a.icon_url" alt="" width="56" height="56">
              <span><span class="feat-name">{{ a.name }}</span><span class="feat-arch">{{ a.arches.map(archLabelOf).join(' · ') }}</span></span>
            </span>
          </span>
          <span class="feat-sum">{{ a.summary }}</span>
        </router-link>
      </li>
    </ul>
  </section>

  <section aria-labelledby="new">
    <div class="sec-head">
      <h2 id="new">New and updated</h2>
      <router-link v-if="apps.length > NEW_COUNT" to="/apps/" class="see-all">See all {{ apps.length }} apps &rsaquo;</router-link>
    </div>
    <ul class="app-list">
      <li v-for="i in newApps" :key="i.id"><AppCard :item="i" /></li>
    </ul>
  </section>

  <section aria-labelledby="cats">
    <h2 id="cats">Categories</h2>
    <ul class="cat-grid">
      <li v-for="c in categories" :key="c.tag">
        <router-link :to="`/category/${slug(c.tag)}/`" class="card cat">
          <img class="icon" :src="c.icon_url" alt="" width="64" height="64" loading="lazy">
          <span class="cat-name">{{ c.name }}</span>
          <span class="cat-count">{{ c.count }} {{ c.count === 1 ? 'app' : 'apps' }}</span>
        </router-link>
      </li>
    </ul>
  </section>

  <section class="contribute" aria-labelledby="add">
    <h2 id="add">Made in the open</h2>
    <p>Everything here is open source and lives in its own repository. The list itself is a repository too: add your app with
      one pull request.</p>
    <a class="btn-outline" href="https://github.com/Phorepoc/index/blob/main/CONTRIBUTING.md">Add your app</a>
  </section>
</template>
