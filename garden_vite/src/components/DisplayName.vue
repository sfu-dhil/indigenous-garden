<script setup>
import { onMounted, useTemplateRef, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { Tooltip } from 'bootstrap'
import { useMediaStore } from '../stores/media.js'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  number: {
    type: Number,
  },
  muted: {
    type: Boolean,
    default: false,
  },
  bold: {
    type: Boolean,
    default: false,
  },
  iconColor: {
    type: String,
  },
  iconTitle: {
    type: String,
  },
  withAudio: {
    type: Boolean,
    default: false,
  },
})

const mediaStore = useMediaStore()
const {
  currentAudio,
} = storeToRefs(mediaStore)

const iconEl = useTemplateRef('icon-el')
const audioPlaying = computed(() => props.withAudio && props.item.audio && currentAudio.value === props.item.audio)

onMounted(() => {
  if (iconEl.value) { new Tooltip(iconEl.value) }
})
</script>

<template>
  <div>
    <span v-if="number" class="pe-1">{{ number }}.</span>
    <i ref="icon-el" v-if="iconColor && iconTitle"
       class="bi bi-circle-fill fs-6 pe-1" :style="`color: ${iconColor}`" :title="iconTitle"
       data-bs-toggle="tooltip" data-bs-html="true" data-bs-placement="bottom"></i>
    <span :class="`${muted ? 'fw-lighter fst-italic fs-6' : ''} ${bold ? 'fw-bolder' : ''}`">
      {{ item.name }}
      <span v-if="item.descriptor" class="small text-muted">({{ item.descriptor }})</span>
      <i v-if="withAudio && item.audio"
        class="click-audio-player bi bi-volume-up-fill ps-1" :class="`${audioPlaying ? 'text-primary' : ''}`"
        @click="() => mediaStore.toggleAudio(item.audio)"
      ></i>
    </span>
  </div>
</template>

