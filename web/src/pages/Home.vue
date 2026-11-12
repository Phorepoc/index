<script setup>
import { banner, newApps, apps, featured, self, NEW_COUNT } from '../data.js'
import AppCard from '../components/AppCard.vue'
import DownloadMenu from '../components/DownloadMenu.vue'
import FeaturedCarousel from '../components/FeaturedCarousel.vue'
const base = import.meta.env.BASE_URL
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
    <h2 id="feat">Featured</h2>
    <FeaturedCarousel :items="featured" />
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

  <section class="contribute" aria-labelledby="add">
    <h2 id="add">Made in the open</h2>
    <p>Everything here is open source and lives in its own repository. The list itself is a repository too: add your app with
      one pull request.</p>
    <a class="btn-outline" href="https://github.com/Phorepoc/index/blob/main/CONTRIBUTING.md">Add your app</a>
  </section>
</template>
