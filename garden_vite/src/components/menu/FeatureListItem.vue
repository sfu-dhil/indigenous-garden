<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useDisplaySetting } from '../../stores/display.js'
import { useMapStore } from '../../stores/map.js'
import DisplayName from '../DisplayName.vue'

const store = useDisplayStore()
const {
  canEdit,
} = useDisplaySetting()
const mapStore = useMapStore()
const {
  hoverId,
} = storeToRefs(mapStore)

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const firstImage = computed(() => props.item.images.length > 0 ? props.item.images[0] : null)
const hoverClass = computed(() => hoverId.value == props.item.id ? 'card-hover' : '')
</script>

<template>
  <div class="card mt-3 w-100" :class="hoverClass" @mouseover="() => hoverId = item.id" @mouseout="() => hoverId = null">
    <img v-if="firstImage" :src="firstImage.thumbnail" class="card-img-top object-fit-cover" loading="lazy" />
    <div class="g-0 card-body">
      <DisplayName v-for="(name, index) in item.english_names" :item="name" :bold="true" :number="index == 0 ? item.number : null" />
      <DisplayName v-for="name in item.western_scientific_names" :item="name" :muted="true" />
      <div class="row g-0">
        <div class="col first-nations-unicode">
          <DisplayName v-for="name in item.halkomelem_names" :item="name" iconColor="#64c4cf" iconTitle="hən̓q̓əmin̓əm̓" />
        </div>
        <div class="col first-nations-unicode">
          <DisplayName v-for="name in item.squamish_names" :item="name" iconColor="#7cb341" iconTitle="Sḵwx̱wú7mesh Sníchim" />
        </div>
      </div>
      <a href="javascript:" @click="() => store.showFeature(item.id)" class="stretched-link"></a>
    </div>
  </div>
  <ul class="nav nav-pills nav-fill" v-if="canEdit">
    <li class="nav-item">
      <a :href="`/admin/garden/feature/${item.id}/change/`" class="nav-link">
        <i class="bi bi-pencil-square" aria-hidden="true"></i> Edit feature
      </a>
    </li>
  </ul>
</template>

<style lang="scss" scoped>
.card img {
  max-height: 200px;
}
.card.card-hover {
  --bs-border-opacity: 1;
  border-color: rgba(var(--bs-primary-rgb),var(--bs-border-opacity)) !important;
}
</style>