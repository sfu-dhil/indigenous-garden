<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { toggleOffcanvas } from '../../helpers/utils.js'
import FeatureListItem from './FeatureListItem.vue'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    required: true,
  },
})
const shown = defineModel('shown')
const offCanvasEl = useTemplateRef('menu-el')

watch(shown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, shown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => shown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => shown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">{{ label }}</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <FeatureListItem v-for="item in items" :item="item"></FeatureListItem>
    </div>
  </div>
</template>