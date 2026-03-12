<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useInterfaceContentStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuIndianResidentialSchoolsMapShown,
} = storeToRefs(displayStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  residentialSchoolsContent,
} = storeToRefs(interfaceContentStore)

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
      <h2 class="offcanvas-title h5" v-html="residentialSchoolsContent.heading" />
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuIndianResidentialSchoolsMapShown">
      <figure class="figure w-100" v-if="residentialSchoolsContent.image">
        <img class="figure-img w-100 object-fit-contain m-0"
              loading="lazy" fetchpriority="low"
              :alt="residentialSchoolsContent.image_caption"
              :src="residentialSchoolsContent.image">
        <figcaption class="figure-caption text-center" v-if="residentialSchoolsContent.image_caption" v-html="residentialSchoolsContent.image_caption" />
      </figure>
      <div v-if="residentialSchoolsContent.content" v-html="residentialSchoolsContent.content" />
    </div>
  </div>
</template>