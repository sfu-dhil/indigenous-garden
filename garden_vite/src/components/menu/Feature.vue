<script setup>
import { ref, useTemplateRef, onMounted, watch, computed, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'
import { useDataStore } from '../../stores/data.js'
import { useDisplayStore, useDisplaySettingStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { useMediaStore } from '../../stores/media.js'
import DisplayName from '../DisplayName.vue'
import 'vidstack/player'
import 'vidstack/player/layouts'
import 'vidstack/player/ui'
import HLS from 'hls.js';

const displayStore = useDisplayStore()
const {
  menuFeatureShown,
  selectedFeatureId,
  selectedPointId,
  selectedGalleryIndex,
} = storeToRefs(displayStore)
const mediaStore = useMediaStore()
const displaySettingStore = useDisplaySettingStore()
const {
  canEdit,
} = storeToRefs(displaySettingStore)

const offCanvasEl = useTemplateRef('menu-el')
const mediaPlayer = useTemplateRef('media-player-el')

const mediaPlayerProviderChange = (event) => {
  const provider = event.detail
  if (provider?.type === 'hls') {
    provider.library = HLS
    // provider.config = { debug: true, }
  }
}

const feature = computed(() => selectedFeatureId.value ? useDataStore().getFeature(selectedFeatureId.value) : null)
const editPointHref = computed(() => {
  if (canEdit.value) {
    let pointType = 'point' // overhead
    if (displaySettingStore.isOverheadViewLocked()) {
      pointType = 'point'
    } else if (displaySettingStore.isPanoramaLocation1ViewLocked()) {
      pointType = 'location1panoramapoint'
    } else if (displaySettingStore.isPanoramaLocation2ViewLocked()) {
      pointType = 'location2panoramapoint'
    } else if (displaySettingStore.isPanoramaLocation3ViewLocked()) {
      pointType = 'location3panoramapoint'
    }
    return `/admin/garden/${pointType}/${ selectedPointId.value }/change/`
  }
  return null
})

watch(menuFeatureShown, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    toggleOffcanvas(offCanvasEl.value, newValue)
    if (newValue === false) {
      selectedFeatureId.value = null
      selectedPointId.value = null
      mediaStore.stopAllMedia()
      mediaPlayer?.value?.pause()
    }
  }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuFeatureShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuFeatureShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuFeatureShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div v-if="feature" class="offcanvas-header">
      <div class="row w-100">
        <div class="col-sm">
          <DisplayName v-for="name in feature.english_names" :item="name" :bold="true" :withAudio="true" />
          <DisplayName v-for="name in feature.western_scientific_names" :item="name" :muted="true" :withAudio="true" />
        </div>
        <div class="col first-nations-unicode">
          <DisplayName v-for="name in feature.halkomelem_names" :item="name" :withAudio="true" iconColor="#64c4cf" iconTitle="hən̓q̓əmin̓əm̓" />
        </div>
        <div class="col first-nations-unicode">
          <DisplayName v-for="name in feature.squamish_names" :item="name" :withAudio="true" iconColor="#7cb341" iconTitle="Sḵwx̱wú7mesh Sníchim" />
        </div>
      </div>
      <button type="button" class="btn-close mb-auto" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div v-if="feature" class="offcanvas-body">
      <div class="row row-cols-4 g-2">
        <div v-for="(image, index) in feature.images" class="col feature-gallery-image p-0 m-0"
            :title="image.description" @click="() => selectedGalleryIndex = index">
          <button type="button" class="btn p-0 m-0 position-relative w-100 h-100 text-primary"
              data-bs-toggle="modal" data-bs-target="#feature-gallery-modal">
            <img :src="image.thumbnail" class="object-fit-cover" :alt="image.description" />
            <div class="position-absolute top-0 bottom-0 start-0 end-0 overlay"></div>
            <i class="bi bi-search position-absolute top-50 start-50 translate-middle"></i>
          </button>
        </div>
      </div>
      <h2 class="my-3">
        {{ feature.feature_type == "PLANT" ? 'Plant Storytelling' : 'Storytelling' }}
      </h2>

      <div class="my-3" v-if="feature.video">
        <media-player
          ref="media-player-el" title="Plant Storytelling" streamType="on-demand"
          :poster="feature.video_thumbnail" keep-alive :autoQuality="true"
          @provider-change="mediaPlayerProviderChange"
        >
          <media-provider>
            <media-poster class="vds-poster"></media-poster>
            <source :src="feature.video" type="application/vnd.apple.mpegurl" />
          </media-provider>
          <media-video-layout :thumbnails="feature.video_thumbnails_vtt"></media-video-layout>
        </media-player>
      </div>
      <div class="my-3" v-html="feature.content"></div>

      <h2 v-if="feature.references" class="my-3">Acknowledgements</h2>
      <div v-if="feature.references" class="my-3" v-html="feature.references"></div>

      <hr v-if="canEdit" />
      <div v-if="canEdit" class="d-grid gap-2 d-md-flex justify-content-md-end">
        <a :href="`/admin/garden/feature/${ feature.id }/change/`" class="btn btn-primary ms-auto">
          <i class="bi bi-pencil-square" aria-hidden="true"></i> Edit feature
        </a>
        <a v-if="selectedPointId" :href="editPointHref" class="btn btn-primary">
          <i class="bi bi-pencil-square" aria-hidden="true"></i> Edit point
        </a>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.feature-gallery-image {
  .btn {
    overflow: hidden;
  }
  img {
    max-height: 110px;
    width: 100%;
    transition: all 0.6s;
  }
  i {
    visibility: hidden;
    font-size: 1em;
    transition: all .6s;
  }
  .overlay {
    background-color: rgba(var(--bs-body-bg-rgb), 0.5);
    display: none;
  }
  &:hover {
    img {
      transform: scale(1.15);
    }
    i {
      visibility: visible;
      font-size: 1.5em;
    }
    .overlay {
      display: inline-block !important;
      font-size: 1.5em;
    }
  }
}
</style>


