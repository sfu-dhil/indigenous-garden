<script setup>
import { useTemplateRef, onMounted, computed, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useData } from '../../stores/data.js'
import { useDisplayStore } from '../../stores/display.js'
import { Tooltip } from 'bootstrap'

const {
  featureMap,
} = useData()
const store = useDisplayStore()
const {
  selectedFeatureId,
} = storeToRefs(store)

const iconElArray = useTemplateRef('icon-el')

const feature = computed(() => selectedFeatureId.value && featureMap.get(selectedFeatureId.value) ? featureMap.get(selectedFeatureId.value) : null)

const refreshTooltips = () => {
  if (iconElArray.value) {
    iconElArray.value.forEach(iconEl => {
      new Tooltip(iconEl)
    })
  }
}
watch(selectedFeatureId, (newValue, oldValue) => {
  if (newValue !== oldValue) { nextTick(refreshTooltips) }
})
onMounted(() => {
  nextTick(refreshTooltips)
})
</script>

<template>
  <div v-if="feature" ref="gallery-el" id="feature-gallery-modal" class="modal fade" tabindex="-1" data-bs-backdrop="static">
    <div class="modal-dialog modal-fullscreen">
      <div class="modal-content">
        <div class="modal-body p-0">
          <button type="button" class="btn-close bg-white position-fixed top-0 end-0 m-3 p-2" data-bs-dismiss="modal" aria-label="Close"></button>
          <div id="feature-gallery-carousel" class="carousel slide h-100" data-bs-ride="false">
            <div class="carousel-inner h-100">
              <div v-for="(image, index) in feature.images" class="carousel-item text-center h-100" :class="`${index == 0 ? 'active' : ''}`">
                <img :src="image.image" class="img-fluid h-100 object-fit-contain mx-auto" loading="lazy"
                    :alt="image.description" :title="image.description" />
                <div class="carousel-caption">
                  <h5 class="d-inline-block px-3 py-2">
                    {{ index+1 }} of {{ feature.images.length }}
                    <i ref="icon-el" v-if="image.license" class="bi bi-info-circle" :title="image.license"
                      data-bs-toggle="tooltip" data-bs-html="true" data-bs-placement="top"
                    ></i>
                  </h5>
                </div>
              </div>
            </div>
            <div class="carousel-indicators">
              <button v-for="(image, index) in feature.images" type="button" data-bs-target="#feature-gallery-carousel" :data-bs-slide-to="index" :class="`${index == 0 ? 'active' : ''}`"></button>
            </div>
            <button type="button" class="carousel-control-prev" data-bs-target="#feature-gallery-carousel" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button type="button" class="carousel-control-next" data-bs-target="#feature-gallery-carousel" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#feature-gallery-modal {
  --bs-modal-bg: transparent;

  .btn-close {
    --bs-btn-close-opacity: 1;
    z-index: calc(var(--bs-modal-zindex) + 5);
  }
}
#feature-gallery-carousel {
  .carousel-item img {
    height: 100vmin;
  }
  .carousel-caption h5 {
    background-color: rgba(0,0,0,0.25);
    color: #fff !important;
  }

  .carousel-control-next-icon,
  .carousel-control-prev-icon {
    background-color: rgba(255,255,255,0.5);
    height: 4rem;
    width: 4rem;
    filter: none;
  }
  .carousel-indicators [data-bs-target] {
    background-color: #fff !important;
  }
}
</style>


