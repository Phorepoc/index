<script setup>
import { archLabel } from '../data.js'
defineProps({ item: { type: Object, required: true } })
</script>

<template>
  <router-link :to="`/app/${item.id}/`" class="card app-card">
    <img class="icon" :src="item.icon_url" alt="" width="64" height="64" loading="lazy">
    <span class="app-text">
      <span class="app-name">{{ item.name }}</span>
      <span class="app-sum">{{ item.summary }}</span>
      <span class="app-meta"><span v-for="a in item.arches" :key="a" class="arch">{{ archLabel({ arches: [a] }) }}</span> {{ item.license }}</span>
    </span>
  </router-link>
</template>
