<script setup>
import { apps } from '../data.js'
import AppCard from '../components/AppCard.vue'
</script>

<template>
  <nav class="crumbs" aria-label="Breadcrumb"><router-link to="/">Phorepoc Catalogue</router-link> / <span>All apps</span></nav>
  <h1>All apps</h1>
  <p class="muted">{{ apps.length }} apps, newest first.</p>
  <ul class="app-list">
    <li v-for="i in apps" :key="i.id"><AppCard :item="i" /></li>
  </ul>
</template>
