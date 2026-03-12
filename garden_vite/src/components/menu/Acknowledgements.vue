<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useInterfaceContentStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuAcknowledgementsShown,
} = storeToRefs(displayStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  acknowledgementsContent,
} = storeToRefs(interfaceContentStore)

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
      <h2 class="offcanvas-title h5" v-html="acknowledgementsContent.heading" />
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuAcknowledgementsShown">
      <div v-html="acknowledgementsContent.content" />

      <div v-for="content_block in acknowledgementsContent.content_blocks">
        <hr class="my-4" />
        <h4 v-html="content_block.heading" />
        <ul class="list-group mb-3" v-if="content_block.list.length > 0">
          <li class="list-group-item list-group-item-action first-nations-unicode" v-for="list_item in content_block.list" v-html="list_item" />
        </ul>
        <div v-html="content_block.content" />
      </div>
    </div>
  </div>
</template>
