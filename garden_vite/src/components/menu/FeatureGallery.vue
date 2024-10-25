<script setup>
import { useTemplateRef, onMounted, computed, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useData } from '../../stores/data.js'
import { useDisplayStore } from '../../stores/display.js'
import { Tooltip, Carousel } from 'bootstrap'

const {
  featureMap,
} = useData()
const store = useDisplayStore()
const {
  selectedFeatureId,
  selectedGalleryIndex,
} = storeToRefs(store)

const iconElArray = useTemplateRef('icon-el')
const carouselItemElArray = useTemplateRef('carousel-item-el')
const carouselIndicatorElArray = useTemplateRef('carousel-indicator-el')
const carouselEl = useTemplateRef('carousel-el')

const feature = computed(() => selectedFeatureId.value && featureMap.get(selectedFeatureId.value) ? featureMap.get(selectedFeatureId.value) : null)

const carouselTo = (to) => {
  const bsCarouse = Carousel.getOrCreateInstance(carouselEl.value)
  bsCarouse.to(to)
}
const carouselPrev = () => {
  const bsCarouse = Carousel.getOrCreateInstance(carouselEl.value)
  bsCarouse.prev()
}
const carouselNext = () => {
  const bsCarouse = Carousel.getOrCreateInstance(carouselEl.value)
  bsCarouse.next()
}
const toggleActiveClass = (el, isActive) => {
  isActive ? el.classList.add("active") : el.classList.remove("active")
}
const updateCarouselActive = () => {
  carouselItemElArray.value.forEach((carouselItemEl, index) => toggleActiveClass(carouselItemEl, index === selectedGalleryIndex.value))
  carouselIndicatorElArray.value.forEach((carouselItemEl, index) => toggleActiveClass(carouselItemEl, index === selectedGalleryIndex.value))
}
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
watch(selectedGalleryIndex, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCarouselActive() }
})
onMounted(() => {
  nextTick(refreshTooltips)
  updateCarouselActive()
  const bsCarouse = Carousel.getOrCreateInstance(carouselEl.value)
  carouselEl.value.addEventListener('slid.bs.carousel', event => {
    selectedGalleryIndex.value = event.to
  })
})
</script>

<template>
  <div v-if="feature" ref="gallery-el" id="feature-gallery-modal" class="modal fade" tabindex="-1" data-bs-backdrop="static">
    <div class="modal-dialog modal-fullscreen">
      <div class="modal-content">
        <div class="modal-body p-0">
          <button type="button" class="btn-close bg-white position-fixed top-0 end-0 m-3 p-2" data-bs-dismiss="modal" aria-label="Close"></button>
          <div ref="carousel-el" class="carousel slide h-100" data-bs-ride="false">
            <div class="carousel-inner h-100">
              <div ref="carousel-item-el" v-for="(image, index) in feature.images" class="carousel-item text-center h-100">
                <img :src="image.image" class="img-fluid h-100 object-fit-contain mx-auto" :alt="image.description" :title="image.description" />
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
              <button ref="carousel-indicator-el" v-for="(image, index) in feature.images" type="button" @click="() => carouselTo(index)" data-bs-target="" :data-bs-slide-to="index"></button>
            </div>
            <button type="button" class="carousel-control-prev" @click="carouselPrev" data-bs-target="" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button type="button" class="carousel-control-next" @click="carouselNext" data-bs-target="" data-bs-slide="next">
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
.carousel {
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


