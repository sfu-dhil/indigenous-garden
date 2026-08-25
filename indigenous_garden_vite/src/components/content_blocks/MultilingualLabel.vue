<script setup>
import { onMounted, computed, ref, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { resetTooltips } from '../../_utils.js'
import { useAudioLabelMediaStore } from '../../stores/display.js'

const {
  currentAudio,
} = storeToRefs(useAudioLabelMediaStore())

const props = defineProps({
  object: {
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

const containerRef = ref()
const audioPlaying = computed(() => props.withAudio && props.object.audio && currentAudio.value === props.object.audio)

onMounted(() => {
  nextTick(() => resetTooltips(containerRef.value))
})
</script>

<template>
  <div ref="containerRef">
    <span v-if="number" class="pe-1">{{ number }}.</span>
    <i v-if="iconColor && iconTitle"
       class="bi bi-circle-fill fs-6 pe-1" :style="`color: ${iconColor}`" :title="iconTitle"
       data-bs-toggle="tooltip" data-bs-html="true" data-bs-placement="bottom"></i>
    <span :class="`${muted ? 'fw-lighter fst-italic fs-6' : ''} ${bold ? 'fw-bolder' : ''}`">
      {{ object.label }}
      <span v-if="object.descriptor" class="small text-muted">({{ object.descriptor }})</span>
      <i v-if="withAudio && object.audio"
        class="click-audio-player bi bi-volume-up-fill ps-1" :class="`${audioPlaying ? 'text-primary' : ''}`"
        @click="() => useAudioLabelMediaStore().toggleAudio(object.audio)"
      ></i>
    </span>
  </div>
</template>

