<script setup>
import { banner, categories, items, slug } from '../data.js'
import AppCard from '../components/AppCard.vue'
</script>

<template>
  <section class="hero">
    <h1>{{ banner.title }}</h1>
    <p>{{ banner.text }}</p>
  </section>
  <section aria-labelledby="cats">
    <h2 id="cats">Categories</h2>
    <ul class="cat-grid">
      <li v-for="c in categories" :key="c.tag">
        <router-link :to="`/category/${slug(c.tag)}/`" class="card cat">
          <img class="icon" :src="c.icon_url" alt="" width="64" height="64" loading="lazy">
          <span class="cat-name">{{ c.name }}</span>
          <span class="cat-count">{{ c.count }} {{ c.count === 1 ? 'item' : 'items' }}</span>
        </router-link>
      </li>
    </ul>
  </section>
  <section aria-labelledby="all">
    <h2 id="all">New and all apps</h2>
    <ul class="app-list">
      <li v-for="i in items" :key="i.id"><AppCard :item="i" /></li>
    </ul>
  </section>
</template>
