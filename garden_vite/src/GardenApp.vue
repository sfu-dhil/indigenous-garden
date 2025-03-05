<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import GardenMap from './components/GardenMap.vue'
import GardenPanoramaVideo from './components/GardenPanoramaVideo.vue'
import ModalWelcomeMessage from './components/ModalWelcomeMessage.vue'
import Menu from './components/Menu.vue'
import { useDisplayStore, useDisplaySettingStore } from './stores/display.js'
import { useDataStore } from './stores/data.js'

const props = defineProps({
  features: {
    type: Array,
    required: true,
  },
  displayOptions: {
    type: Object,
    required: true,
  },
})

const displaySettingStore = useDisplaySettingStore()
const {
  canEdit,
  isEditMode,
  editPointId,
} = storeToRefs(displaySettingStore)
const displayStore = useDisplayStore()
const {
  panoramaViewShown,
} = storeToRefs(displayStore)
const dataStore = useDataStore()
const {
  features,
} = storeToRefs(dataStore)

// setup init data
canEdit.value = !!props.displayOptions.canEdit
isEditMode.value = !!props.displayOptions.isEditMode
editPointId.value = props.displayOptions.editPointId
features.value = props.features
if (canEdit.value) {
  panoramaViewShown.value = false
}

const displayMap = computed(() => panoramaViewShown.value ? 'd-none' : 'd-block')
const displayPanorama = computed(() => panoramaViewShown.value ? 'd-block' : 'd-none')
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
  color: #dee2e6;
  background-color: #212529;

  &::v-deep {
    @import 'bootstrap/scss/bootstrap.scss';

    .modal {
      --bs-modal-zindex: 1100;
    }
  }
}
</style>
