<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useInfoPageStore } from '../stores/data.js'
import { useDisplayStore, FeatureFilterTypes } from '../stores/display.js'
import { toggleOffcanvas } from '../_utils.js'

const {
  menuSidebarShown: shown,
  infoPageIdShown: shownInfoPageId,
} = storeToRefs(useDisplayStore())

const infoPages = await useInfoPageStore().getAll()
const offCanvasRef = ref(null)

watch(shown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasRef.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasRef.value, shown.value)
  offCanvasRef.value.addEventListener('hidden.bs.offcanvas', () => shown.value = false)
  offCanvasRef.value.addEventListener('shown.bs.offcanvas', () => shown.value = true)
})
const handleClick = (object) => {
  if (object.title === 'Plants') {
    useDisplayStore().showFeatureSelectionSidebar(FeatureFilterTypes.plant)
  } else if (object.title === 'Features'){
    useDisplayStore().showFeatureSelectionSidebar(FeatureFilterTypes.gardenFeature)
  } else if (object.id !== shownInfoPageId ) {
    useDisplayStore().showInfoPage(object)
  }
}
</script>

<template>
  <div ref="offCanvasRef" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Indigenous Garden Interactive Map</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="shown">
      <ul class="nav nav-pills flex-column">
        <li v-for="object in infoPages" :key="object.id"class="nav-item">
          <button
            class="nav-link text-start"
            @click="() => handleClick(object)"
          >
            <i :class="object.properties.list_icon" v-if="object.properties.list_icon" />
            {{ object.title }}
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.offcanvas {
  width: 500px;
  background-color: rgba(var(--bs-secondary-bg-rgb),1) !important;
}
/* mimic active on hover */
.offcanvas .nav-pills .nav-link:hover {
  color: #fff;
  background-color: #0d6efd;
}
</style>