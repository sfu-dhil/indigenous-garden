<script setup>
import { computed, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import GardenMap from './components/GardenMap.vue'
import GardenPanoramaVideo from './components/GardenPanoramaVideo.vue'
import ModalWelcomeMessage from './components/ModalWelcomeMessage.vue'
import Menu from './components/Menu.vue'
import { useDisplayStore, useDisplaySetting } from './stores/display'

const displayStore = useDisplayStore()
const {
  panoramaViewShown,
} = storeToRefs(displayStore)
const {
  canEdit,
  isEditMode,

} = useDisplaySetting()

const displayMap = computed(() => panoramaViewShown.value ? 'd-none' : 'd-block')
const displayPanorama = computed(() => panoramaViewShown.value ? 'd-block' : 'd-none')
onMounted(() => {
  if (canEdit) {
    panoramaViewShown.value = false
  }
})
</script>

<template>
  <div class="app-wrapper" data-bs-theme="dark">
    <GardenMap :class="displayMap"></GardenMap>
    <GardenPanoramaVideo v-if="!isEditMode" :class="displayPanorama"></GardenPanoramaVideo>
    <Menu v-if="!isEditMode"></Menu>
    <ModalWelcomeMessage v-if="!isEditMode"></ModalWelcomeMessage>
  </div>
</template>

<style lang="scss" scoped>
.app-wrapper {
  height: 100%;
  width: 100%;
  min-height: 700px;
  position: relative;
  overflow: hidden;

  &::v-deep {
    @import 'bootstrap/scss/bootstrap.scss';

    .modal {
      --bs-modal-zindex: 1100;
    }
  }
}
</style>
