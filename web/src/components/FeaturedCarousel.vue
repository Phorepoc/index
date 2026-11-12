<script setup>
// The featured carousel: a looping track (the list three times over) that centres one card; the cards to either side
// fade out through a mask on the viewport. It advances on its own every few seconds, pauses while the pointer, a touch
// or the keyboard focus is on it, and does not move by itself (nor animate) with prefers-reduced-motion. Arrows and a
// horizontal swipe move it by one card.
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { archLabelOf } from '../data.js'
const props = defineProps({ items: { type: Array, required: true }, interval: { type: Number, default: 4500 } })
const n = props.items.length
const track = computed(() => [...props.items, ...props.items, ...props.items])
const pos = ref(n)                 // index into the track of the centred card (always within the middle copy at rest)
const animate = ref(true)
const paused = ref(false)
let timer = null
let reduced = false
let touchX = null

const go = (d) => { animate.value = !reduced; pos.value += d; if (reduced) wrap() }
function wrap() {
  // after the move: jump back into the middle copy without animation, so the loop has no end
  if (pos.value < n || pos.value >= 2 * n) {
    animate.value = false
    pos.value = n + (((pos.value - n) % n) + n) % n
  }
}
const pause = () => { paused.value = true }
const resume = () => { paused.value = false }
function touchStart(e) { pause(); touchX = e.touches[0].clientX }
function touchEnd(e) {
  if (touchX !== null) {
    const dx = e.changedTouches[0].clientX - touchX
    if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1)
  }
  touchX = null
  resume()
}
onMounted(() => {
  reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!reduced && n > 1) timer = setInterval(() => { if (!paused.value && !document.hidden) go(1) }, props.interval)
})
onBeforeUnmount(() => clearInterval(timer))
const active = computed(() => ((pos.value - n) % n + n) % n)
</script>

<template>
  <div class="carousel" aria-roledescription="carousel" aria-label="Featured apps"
       @mouseenter="pause" @mouseleave="resume" @focusin="pause" @focusout="resume"
       @touchstart.passive="touchStart" @touchend="touchEnd">
    <div class="arrows">
      <button type="button" class="arrow" aria-label="Previous app" @click="go(-1)">&lsaquo;</button>
      <button type="button" class="arrow" aria-label="Next app" @click="go(1)">&rsaquo;</button>
    </div>
    <div class="car-view">
      <ul class="car-track" :class="{ still: !animate }" :style="{ '--pos': pos }" @transitionend="wrap">
        <li v-for="(a, k) in track" :key="k" :class="{ on: k === pos }" :aria-hidden="k === pos ? 'false' : 'true'">
          <router-link :to="`/app/${a.id}/`" class="card feat-card" :tabindex="k === pos ? 0 : -1">
            <img class="icon" :src="a.icon_url" alt="" width="72" height="72">
            <span class="feat-name">{{ a.name }}</span>
            <span class="feat-arch"><span v-for="x in a.arches" :key="x" class="arch">{{ archLabelOf(x) }}</span></span>
            <span class="feat-sum">{{ a.summary }}</span>
          </router-link>
        </li>
      </ul>
    </div>
    <p class="car-dots" aria-hidden="true"><span v-for="(a, k) in items" :key="a.id" :class="{ on: k === active }" /></p>
  </div>
</template>
