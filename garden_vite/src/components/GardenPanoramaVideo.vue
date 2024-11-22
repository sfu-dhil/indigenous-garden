

<script setup>
import { ref, useTemplateRef, onMounted, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../stores/display.js'
import videojs from 'video.js'
import 'videojs-vr'

const displayStore = useDisplayStore()
const {
  panoramaViewShown,
} = storeToRefs(displayStore)

const videoEl = useTemplateRef('panorama-video')
const player = ref(null)
const wasPlaying = ref(false)

watch(panoramaViewShown, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (!newValue) {
      wasPlaying.value = !player.value.paused()
      player.value.pause()
    } else {
      nextTick(() => {
        player.value.vr().handleResize_() // fixes video not loading properly when switching views
        if (wasPlaying.value) { player.value.play() }
      })
    }
  }
})
onMounted(() => {
  player.value = videojs(videoEl.value)
  player.value.vr({projection: '360'})
})
const updateFov = (delta) => {
  const MIN_FOV = 30
  const MAX_FOV = 110
  if (player.value.vr().camera.fov + delta >= MIN_FOV && player.value.vr().camera.fov + delta <= MAX_FOV) {
    player.value.vr().camera.fov += delta;
    player.value.vr().camera.updateProjectionMatrix();
  }
}
</script>

<template>
  <div @wheel="(e) => updateFov(e.deltaY * 0.01)" class="garden-panorama" :class="panoramaViewShown ? 'd-block' : 'd-none'">
    <div class=" ol-zoom ol-unselectable ol-control text-secondary">
      <button @click="() => updateFov(-10)" type="button" class="ol-zoom-in" title="Zoom in">+</button>
      <button @click="() => updateFov(10)" type="button" class="ol-zoom-out" title="Zoom out">–</button>
    </div>
    <div class="show-menu-control ol-unselectable ol-control text-secondary">
      <button @click="() => displayStore.showMainMenu()" type="button" title="Show Menu">
        <i class="bi bi-list-ol"></i>
      </button>
    </div>
    <div class="show-welcome-control ol-unselectable ol-control text-secondary">
      <button @click="() => displayStore.showWelcomeMessage()" type="button" title="Show Welcome Message">
        <i class="fa-solid fa-message"></i>
      </button>
    </div>
    <div class="select-view-control ol-unselectable ol-control text-secondary">
      <button type="button" @click="() => displayStore.showMapView()" title="Panorama view. Click to switch to Map view">
        <i class="bi bi-pin-map-fill"></i>
      </button>
    </div>
    <video ref="panorama-video" class="video-js vjs-fluid vjs-default-skin vjs-big-play-centered" preload="metadata" controls loop muted>
      <source :src="'/static/videos/panorama.webm'" type="video/webm"></source>
    </video>
  </div>
</template>

<style lang="scss" scoped>
.garden-panorama {
  height: 100%;
  width: 100%;

  .ol-control  {
    z-index: 100 !important;
    pointer-events: auto;
  }
  .ol-control button {
    font-size: 1.5em;
    pointer-events: auto;
  }
  .ol-button i {
    color: inherit;
  }
  .show-menu-control {
    left: .5em;
    top: 5.0em;
    z-index: 2;
  }
  .show-welcome-control {
    left: .5em;
    top: 7.5em;
    z-index: 2;
  }
  .select-view-control {
    left: .5em;
    top: 10em;
    z-index: 2;
  }
}
</style>