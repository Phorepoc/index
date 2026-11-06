<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { search } from '../data.js'
import AppCard from '../components/AppCard.vue'
const route = useRoute()
const q = computed(() => String(route.query.q || ''))
const results = computed(() => search(q.value))
</script>

<template>
  <h1>Search</h1>
  <p v-if="!q.trim()" class="muted">Type in the search box to look for an app by name, tag or description.</p>
  <template v-else>
    <p role="status" class="muted">{{ results.length }} {{ results.length === 1 ? 'result' : 'results' }} for "{{ q }}"</p>
    <ul class="app-list">
      <li v-for="i in results" :key="i.id"><AppCard :item="i" /></li>
    </ul>
  </template>
</template>
