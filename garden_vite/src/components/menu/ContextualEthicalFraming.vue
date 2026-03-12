<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useInterfaceContentStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuContextualEthicalFramingShown,
} = storeToRefs(displayStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  contextualEthicalFramingContent,
} = storeToRefs(interfaceContentStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuContextualEthicalFramingShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuContextualEthicalFramingShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuContextualEthicalFramingShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuContextualEthicalFramingShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5" v-html="contextualEthicalFramingContent.heading" />
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuContextualEthicalFramingShown">
      <div v-if="contextualEthicalFramingContent.content" v-html="contextualEthicalFramingContent.content" />
    </div>
  </div>
</template>
