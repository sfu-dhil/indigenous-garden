<!-- based on https://github.com/jarvisniu/vue-pannellum but modified to work better -->
<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import '../assets/pannellum/pannellum.js'


const viewer = defineModel('viewer')
const src = defineModel('src', { required: true })
const hfov = defineModel('hfov', { default: 75 })
const yaw = defineModel('yaw', { default: 0 })
const pitch = defineModel('pitch', { default: 0 })

const props = defineProps({
  preview: { type: String },
  autoLoad: { type: Boolean, default: true },
  draggable: { type: Boolean, default: true },
  mouseZoom: { type: Boolean, default: true },
  doubleClickZoom: { type: Boolean, default: true },
  showControls: { type: Boolean, default: true },
  compass: { type: Boolean, default: false },
  hotSpots: { type: Array, default: [] },
  minHfov: { type: Number, default: 50 },
  maxHfov: { type: Number, default: 120 },
  crossOrigin: {type: String, default: 'anonymous' },
})

const pannellumRef = ref(null)
const animationFrameId = ref(null)

const srcOption = computed(() => {
  if (typeof src.value === 'string') {
    return {
      type: 'equirectangular',
      panorama: src.value,
      hotSpots: props.hotSpots,
    }
  } else if (typeof src.value === 'object') {
    if (src.value.px && src.value.ny) {
      return {
        type: 'cubemap',
        cubeMap: [
          src.value.pz,
          src.value.px,
          src.value.nz,
          src.value.nx,
          src.value.py,
          src.value.ny,
        ],
        hotSpots: props.hotSpots,
      }
    } else if (src.value.scenes) {
      return {
        default: src.value.default,
        scenes: src.value.scenes,
      }
    } else {
      console.error('[vue-pannellum] Unknown src type')
    }
  } else {
    console.error('[vue-pannellum] Unknown src type: ' + typeof src.value)
  }
})

watch(src, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (viewer.value) { viewer.value.destroy() }
    nextTick(() => loadPannellum())
  }
})
watch(hfov, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (viewer.value) { viewer.value.setHfov(newValue, false) }
  }
})
watch(yaw, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (viewer.value) { viewer.value.setYaw(newValue, false) }
  }
})

const loadPannellum = () => {
  const options = {
    hfov: hfov.value,
    yaw: yaw.value,
    pitch: pitch.value,
    preview: props.preview,
    autoLoad: props.autoLoad,
    draggable: props.draggable,
    mouseZoom: props.mouseZoom,
    doubleClickZoom: props.doubleClickZoom,
    showControls: props.showControls,
    compass: props.compass,
    minHfov: props.minHfov,
    maxHfov: props.maxHfov,
    crossOrigin: props.crossOrigin,
    ...srcOption.value,
  }
  viewer.value = window.pannellum.viewer(pannellumRef.value, options)
}
const animationFrameLoop = () => {
  animationFrameId.value = window.requestAnimationFrame(animationFrameLoop)

  if (viewer.value) {
    const hfovUpdate = viewer.value.getHfov()
    const yawUpdate = viewer.value.getYaw()
    const pitchUpdate = viewer.value.getPitch()
    if (hfovUpdate != hfov.value) { hfov.value = hfovUpdate}
    if (yawUpdate != yaw.value) { yaw.value = yawUpdate}
    if (pitchUpdate != pitch.value) { pitch.value = pitchUpdate}
  }
}

onMounted(() => {
  loadPannellum()
  animationFrameId.value = window.requestAnimationFrame(animationFrameLoop)
})
onUnmounted(() => {
  if (viewer.value) {
    viewer.value.destroy()
    viewer.value = null
  }
  if (animationFrameId.value) { window.cancelAnimationFrame(animationFrameId.value) }
})
</script>

<template>
  <div
    ref="pannellumRef"
    class="vue-pannellum"
    @mouseup="onMouseUp"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
  ></div>
</template>

<style lang="scss" scoped>
// pannellum


.vue-pannellum {
  position: relative;

  &:deep() {
    .pnlm-ui .pnlm-about-msg {
      display: none !important;
    }
  }
}
</style>
