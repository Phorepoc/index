<script setup>
import { computed } from 'vue'
import { categoryBySlug, inCategory } from '../data.js'
import AppCard from '../components/AppCard.vue'
const props = defineProps({ slug: String })
const cat = computed(() => categoryBySlug(props.slug))
const list = computed(() => (cat.value ? inCategory(cat.value.tag) : []))
</script>

<template>
  <nav class="crumbs" aria-label="Breadcrumb"><router-link to="/">Catalogue</router-link> / <span>{{ cat ? cat.name : 'Category' }}</span></nav>
  <template v-if="cat">
    <header class="page-head">
      <img class="icon" :src="cat.icon_url" alt="" width="64" height="64">
      <div>
        <h1>{{ cat.name }}</h1>
        <p class="muted">{{ cat.count }} {{ cat.count === 1 ? 'item' : 'items' }}</p>
      </div>
    </header>
    <ul class="app-list">
      <li v-for="i in list" :key="i.id"><AppCard :item="i" /></li>
    </ul>
  </template>
  <p v-else>No such category. <router-link to="/">Back to the catalogue</router-link></p>
</template>
