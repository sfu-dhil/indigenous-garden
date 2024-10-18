<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { ImgComparisonSlider } from '@img-comparison-slider/vue';
import { loremIpsum } from 'lorem-ipsum'

const store = useDisplayStore()
const {
  menuHistoryShown,
} = storeToRefs(store)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuHistoryShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuHistoryShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuHistoryShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuHistoryShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start position-absolute" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">History</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <figure class="figure w-100">
        <svg class="figure-img w-100 object-fit-contain m-0" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
          <title>Placeholder</title>
          <rect width="100%" height="100%" fill="#20c997"></rect>
          <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Video Placeholder</text>
        </svg>
        <!--  <video src="{{ feature.video.url }}" controls class="figure-img w-100 object-fit-contain m-0" preload="metadata"></video> -->
        <figcaption class="figure-caption text-center">
          The Making of the Indigenous Garden
        </figcaption>
      </figure>

      <figure class="figure w-100">
        <ImgComparisonSlider class="w-100">
          <svg slot="first" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#20c997"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 1 Placeholder</text>
          </svg>
          <svg slot="second" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#868e96"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 2 Placeholder</text>
          </svg>
          <!-- <img slot="first" width="100%" src="images/green-leaves.0ebdd195.webp" loading="lazy" fetchpriority="low"> -->
          <!-- <img slot="second" width="100%" src="images/green-leaves-blurred.6ba79d3a.webp" loading="lazy" fetchpriority="low"> -->
        </ImgComparisonSlider>
        <figcaption class="figure-caption text-center">
          Before and after of the Indigenous Garden
        </figcaption>
      </figure>

      <p>{{ loremIpsum({count: 2, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
    </div>
  </div>
</template>
