<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useInterfaceContentStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { ImgComparisonSlider } from '@img-comparison-slider/vue';
import VideoPlayerWrapper from '../VideoPlayerWrapper.vue'

const displayStore = useDisplayStore()
const {
  menuHistoryShown,
} = storeToRefs(displayStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  historyContent,
} = storeToRefs(interfaceContentStore)

const offCanvasEl = useTemplateRef('menu-el')
const websiteOrigin = window.location.origin

watch(menuHistoryShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuHistoryShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuHistoryShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuHistoryShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5" v-html="historyContent.heading" />
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuHistoryShown">
      <figure class="figure w-100">
        <VideoPlayerWrapper
          :video="websiteOrigin+'/static/videos/introduction_to_history_of_the_garden/master.mpd'"
          title="Introduction to History of the Garden"
          :thumbnail="websiteOrigin+'/static/thumbnails/introduction_to_history_of_the_garden.png'"
          :thumbnails_vtt="websiteOrigin+'/static/thumbnails/introduction_to_history_of_the_garden/thumbnails.vtt'"
        ></VideoPlayerWrapper>
      </figure>
      <div v-if="historyContent.content_1" v-html="historyContent.content_1" />

      <figure class="figure w-100">
        <VideoPlayerWrapper
          :video="websiteOrigin+'/static/videos/ground_breaking_ceremony/master.mpd'"
          title="Ground Breaking Ceremony"
          :thumbnail="websiteOrigin+'/static/thumbnails/ground_breaking_ceremony.png'"
          :thumbnails_vtt="websiteOrigin+'/static/thumbnails/ground_breaking_ceremony/thumbnails.vtt'"
        ></VideoPlayerWrapper>
      </figure>
      <div v-if="historyContent.content_4" v-html="historyContent.content_4" />

      <figure class="figure w-100">
        <VideoPlayerWrapper
          :video="websiteOrigin+'/static/videos/garden_design_and_identifying_the_plants/master.mpd'"
          title="Design & Identifying the Plants"
          :thumbnail="websiteOrigin+'/static/thumbnails/garden_design_and_identifying_the_plants.png'"
          :thumbnails_vtt="websiteOrigin+'/static/thumbnails/garden_design_and_identifying_the_plants/thumbnails.vtt'"
        ></VideoPlayerWrapper>
      </figure>
      <div v-if="historyContent.content_2" v-html="historyContent.content_2" />

      <figure class="figure w-100">
        <VideoPlayerWrapper
          :video="websiteOrigin+'/static/videos/usage_of_the_space/master.mpd'"
          title="Usage of the Space"
          :thumbnail="websiteOrigin+'/static/thumbnails/usage_of_the_space.png'"
          :thumbnails_vtt="websiteOrigin+'/static/thumbnails/usage_of_the_space/thumbnails.vtt'"
        ></VideoPlayerWrapper>
      </figure>
      <div v-if="historyContent.content_3" v-html="historyContent.content_3" />

      <figure class="figure w-100">
        <VideoPlayerWrapper
          :video="websiteOrigin+'/static/videos/future_goals_directions_and_dreams/master.mpd'"
          title="Future Goals, Directions and Dreams"
          :thumbnail="websiteOrigin+'/static/thumbnails/future_goals_directions_and_dreams.png'"
          :thumbnails_vtt="websiteOrigin+'/static/thumbnails/future_goals_directions_and_dreams/thumbnails.vtt'"
        ></VideoPlayerWrapper>
      </figure>
      <div v-if="historyContent.content_5" v-html="historyContent.content_5" />

      <!-- <figure class="figure w-100">
        <ImgComparisonSlider class="w-100">
          <svg slot="first" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#20c997"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 1 Placeholder</text>
          </svg>
          <svg slot="second" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#868e96"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 2 Placeholder</text>
          </svg> -->
          <!-- <img slot="first" width="100%" src="images/green-leaves.0ebdd195.webp" loading="lazy" fetchpriority="low"> -->
          <!-- <img slot="second" width="100%" src="images/green-leaves-blurred.6ba79d3a.webp" loading="lazy" fetchpriority="low"> -->
        <!-- </ImgComparisonSlider>
        <figcaption class="figure-caption text-center">
          Before and after of the Indigenous Garden
        </figcaption>
      </figure> -->
    </div>
  </div>
</template>
