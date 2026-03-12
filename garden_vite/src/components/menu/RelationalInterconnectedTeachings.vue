<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useInterfaceContentStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuRelationalInterconnectedTeachingsShown,
} = storeToRefs(displayStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  relationalInterconnectedTeachingsContent,
} = storeToRefs(interfaceContentStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuRelationalInterconnectedTeachingsShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuRelationalInterconnectedTeachingsShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuRelationalInterconnectedTeachingsShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuRelationalInterconnectedTeachingsShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5" v-html="relationalInterconnectedTeachingsContent.heading" />
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuRelationalInterconnectedTeachingsShown">
      <div v-if="relationalInterconnectedTeachingsContent.content" v-html="relationalInterconnectedTeachingsContent.content" />
    </div>
  </div>
</template>


