<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const store = useDisplayStore()
const {
  menuMainShown,
} = storeToRefs(store)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuMainShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuMainShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuMainShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuMainShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start position-absolute" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Indigenous Garden</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <ul class="nav nav-pills flex-column">
        <li class="nav-item">
          <button @click="() => store.showHistory()" class="nav-link">
            <i class="fa-solid fa-timeline"></i>
            History
          </button>
        </li>
        <li class="nav-item">
          <button @click="() => store.showIndianResidentialSchoolsMap()" class="nav-link">
            <i class="fa-solid fa-children"></i>
            Indian Residential Schools Map
          </button>
        </li>
        <li class="nav-item">
          <button @click="() => store.showPlantList()" class="nav-link">
            <i class="fa-solid fa-seedling"></i>
            Plants
          </button>
        </li>
        <li class="nav-item">
          <button @click="() => store.showFeatureList()" class="nav-link">
            <i class="fa-solid fa-monument"></i>
            Features
          </button>
        </li>
        <li class="nav-item">
          <button @click="() => store.showReferences()" class="nav-link">
            <i class="fa-solid fa-book-open"></i>
            References
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* mimic active on hover */
.offcanvas .nav-pills .nav-link:hover {
  color: #fff;
  background-color: #0d6efd;
}
</style>
