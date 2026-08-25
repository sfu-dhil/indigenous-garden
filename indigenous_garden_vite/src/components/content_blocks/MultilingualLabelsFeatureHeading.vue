<script setup>
import { computed } from 'vue'
import { MultilingualLabelLanguages } from '../../_resourceTypes.js'
import MultilingualLabel from './MultilingualLabel.vue'

const props = defineProps({
  object: { type: Object, required: true },
})

const englishLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.english))
const westernScientificLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.westernScientific))
const halkomelemLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.halkomelem))
const squamishLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.squamish))
</script>

<template>
  <div class="row w-100">
    <div class="col-sm" v-if="englishLabels.length > 0 || westernScientificLabels.length > 0">
      <MultilingualLabel v-for="label in englishLabels" :object="label" :bold="true" :withAudio="true" />
      <MultilingualLabel v-for="label in westernScientificLabels" :object="label" :muted="true" :withAudio="true" />
    </div>
    <div class="col first-nations-unicode" v-if="halkomelemLabels.length > 0">
      <MultilingualLabel v-for="label in halkomelemLabels" :object="label" :withAudio="true" iconColor="#64c4cf" iconTitle="hən̓q̓əmin̓əm̓" />
    </div>
    <div class="col first-nations-unicode" v-if="squamishLabels.length > 0">
      <MultilingualLabel v-for="label in squamishLabels" :object="label" :withAudio="true" iconColor="#7cb341" iconTitle="Sḵwx̱wú7mesh Sníchim" />
    </div>
  </div>
</template>

