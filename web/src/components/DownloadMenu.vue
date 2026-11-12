<script setup>
// The Download button: a menu of the app's packages, one per architecture (the SIS file for that architecture)
import { QBtnDropdown, QList, QItem, QItemSection, QItemLabel, ClosePopup } from 'quasar'
const vClosePopup = ClosePopup
import { archLabelOf, archNoteOf, formatSize } from '../data.js'
defineProps({ app: { type: Object, required: true }, label: { type: String, default: 'Download' } })
</script>

<template>
  <q-btn-dropdown v-if="app.packages.length" unelevated no-caps color="primary" class="dl-btn" :label="label"
                  :aria-label="`${label} ${app.name}: choose the architecture`">
    <q-list class="dl-menu">
      <q-item v-for="p in app.packages" :key="p.url" clickable tag="a" :href="p.url" v-close-popup>
        <q-item-section>
          <q-item-label>{{ archLabelOf(p.arch) }} <span class="muted">&middot; {{ formatSize(p.size) }} &middot; {{ p.tag }}</span></q-item-label>
          <q-item-label caption>{{ archNoteOf(p.arch) }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>
