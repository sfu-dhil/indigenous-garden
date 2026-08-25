<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useFeaturesStore } from '../stores/data.js'
import { useDisplayStore, FeatureFilterTypes } from '../stores/display.js'
import { toggleOffcanvas } from '../_utils.js'
import { ContentBlockResourceTypes, IconResourceTypes } from '../_resourceTypes.js'
import MultilingualLabelsFeatureListHeading from './content_blocks/MultilingualLabelsFeatureListHeading.vue'

const {
  featureSelectionSidebarShown: shown,
  featureSelectionSidebarFilterType: featureFilterType,
  featureIdShown: shownId,
  featureIdHover: hoverId,
} = storeToRefs(useDisplayStore())

const allObjects = await useFeaturesStore().getAll()
const objects = computed(() => allObjects.filter((o) => o.properties.feature_type === featureFilterType.value).map((o) => {
  const image_cb = o.content_blocks.filter((cb) => [ContentBlockResourceTypes.image, ContentBlockResourceTypes.imageGallery].includes(cb.resourcetype))[0] ?? undefined
  if (image_cb && ContentBlockResourceTypes.image === image_cb.resourcetype) {
    o.thumbnail = image_cb.thumbnail
  } else if (image_cb && ContentBlockResourceTypes.imageGallery === image_cb.resourcetype && image_cb.images.length > 0) {
    o.thumbnail = image_cb.images[0].thumbnail
  } else if (o.icon && o.icon.resourcetype === IconResourceTypes.image) {
    o.thumbnail = o.icon.thumbnail
  }
  o.multilingualLabels = o.content_blocks.filter((cb) => ContentBlockResourceTypes.multilingualLabels === cb.resourcetype)[0] ?? undefined
  return o
}))
const offCanvasRef = ref(null)

watch(shown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasRef.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasRef.value, shown.value)
  offCanvasRef.value.addEventListener('hidden.bs.offcanvas', () => shown.value = false)
  offCanvasRef.value.addEventListener('shown.bs.offcanvas', () => shown.value = true)
})
</script>

<template>
  <div ref="offCanvasRef" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5" v-if="featureFilterType === FeatureFilterTypes.plant">Plants</h2>
      <h2 class="offcanvas-title h5" v-if="featureFilterType === FeatureFilterTypes.gardenFeature">Features</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="shown">
      <div v-for="object in objects" :key="object.id"
        class="card mt-3 w-100"
        :class="{ 'hover': hoverId === object.id }"
        @mouseover="() => hoverId = object.id" @mouseout="() => hoverId = null"
      >
        <img
          v-if="object.thumbnail"
          :src="object.thumbnail"
          class="card-img-top object-fit-cover w-100"
          :alt="object.title"
        />
        <div class="g-0 card-body">
          <MultilingualLabelsFeatureListHeading v-if="object.multilingualLabels"
            :object="object.multilingualLabels" :numberLabel="object.icon && object.icon.resourcetype === IconResourceTypes.numbered ? object.icon.number : undefined"
          />
          <a href="javascript:" @click="() => useDisplayStore().showFeature(object)" class="stretched-link"></a>
        </div>
      </div>

<!--
      <div class="d-flex justify-content-between align-items-start">
        <div class="card-body d-flex justify-content-between align-items-start">
          <span
            v-if="object.icon && object.icon.resourcetype === IconResourceTypes.numbered"
            class="fw-bold me-2"
            v-html="`${object.icon.number}.`" />
          <p class="me-auto card-text" v-html="object.title" />
        </div>
      </div>
          -->

    </div>
  </div>
</template>

<style lang="scss" scoped>
.offcanvas {
  width: 450px;
  background-color: rgba(var(--bs-secondary-bg-rgb),1) !important;
}
.card {
  cursor: pointer;
  img {
    max-height: 200px;
  }
  &.hover {
    border-color: rgba(var(--bs-primary-rgb),1) !important;
  }
}
</style>


