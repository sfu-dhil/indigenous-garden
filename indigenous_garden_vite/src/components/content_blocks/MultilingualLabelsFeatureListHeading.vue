<script setup>
import { computed } from 'vue'
import { MultilingualLabelLanguages } from '../../_resourceTypes.js'
import MultilingualLabel from './MultilingualLabel.vue'

const props = defineProps({
  object: { type: Object, required: true },
  numberLabel: { type: Number },
})

const englishLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.english))
const westernScientificLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.westernScientific))
const halkomelemLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.halkomelem))
const squamishLabels = computed(() => props.object.labels.filter((l) => l.language === MultilingualLabelLanguages.squamish))
</script>

<template>
  <MultilingualLabel v-for="(label, index) in englishLabels" :object="label" :bold="true" :number="index == 0 ? numberLabel : null" />
  <MultilingualLabel v-for="label in westernScientificLabels" :object="label" :muted="true" />
  <div class="row g-0">
    <div class="col first-nations-unicode">
      <MultilingualLabel v-for="label in halkomelemLabels" :object="label" iconColor="#64c4cf" iconTitle="hən̓q̓əmin̓əm̓" />
    </div>
    <div class="col first-nations-unicode">
      <MultilingualLabel v-for="label in squamishLabels" :object="label" iconColor="#7cb341" iconTitle="Sḵwx̱wú7mesh Sníchim" />
    </div>
  </div>
</template>

