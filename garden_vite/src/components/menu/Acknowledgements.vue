<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { loremIpsum } from 'lorem-ipsum'

const displayStore = useDisplayStore()
const {
  menuAcknowledgementsShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuAcknowledgementsShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuAcknowledgementsShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuAcknowledgementsShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuAcknowledgementsShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Acknowledgements</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <p>{{ loremIpsum({count: 2, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
      <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
    </div>
  </div>
</template>
