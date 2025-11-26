<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { loremIpsum } from 'lorem-ipsum'

const displayStore = useDisplayStore()
const {
  menuIndianResidentialSchoolsMapShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuIndianResidentialSchoolsMapShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuIndianResidentialSchoolsMapShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuIndianResidentialSchoolsMapShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuIndianResidentialSchoolsMapShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Indian Residential Schools Map</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuIndianResidentialSchoolsMapShown">
      <figure class="figure w-100">
        <img class="figure-img w-100 object-fit-contain m-0"
              loading="lazy" fetchpriority="low"
              alt="Residential Schools of Canada"
              :src="'/static/images/residential-schools-of-canada.webp'">
        <figcaption class="figure-caption text-center">
          Residential Schools of Canada
        </figcaption>
      </figure>

      <figure class="figure w-100">
        <svg class="figure-img w-100 object-fit-contain m-0" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
          <title>Placeholder</title>
          <rect width="100%" height="100%" fill="#20c997"></rect>
          <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Video 1 Placeholder</text>
        </svg>
        <!-- <video src="{{ feature.video.url }}" controls class="figure-img w-100 object-fit-contain m-0" preload="metadata"></video> -->
        <figcaption class="figure-caption text-center">
          Video 1
        </figcaption>
      </figure>

      <figure class="figure w-100">
        <svg class="figure-img w-100 object-fit-contain m-0" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
          <title>Placeholder</title>
          <rect width="100%" height="100%" fill="#20c997"></rect>
          <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Video 2 Placeholder</text>
        </svg>
        <!-- <video src="{{ feature.video.url }}" controls class="figure-img w-100 object-fit-contain m-0" preload="metadata"></video> -->
        <figcaption class="figure-caption text-center">
          Video 2
        </figcaption>
      </figure>

      <p>{{ loremIpsum({count: 2, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
    </div>
  </div>
</template>