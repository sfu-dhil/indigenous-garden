<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import GardenMap from './components/GardenMap.vue'
import PanoramaView from './components/PanoramaView.vue'
import ModalWelcomeMessage from './components/ModalWelcomeMessage.vue'
import Menu from './components/Menu.vue'
import { useDisplayStore, useDisplaySettingStore } from './stores/display.js'
import { usePanoramaStore } from './stores/panorama.js'
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
  lockView,
  canEdit,
  isEditMode,
  editPointId,
} = storeToRefs(displaySettingStore)
const displayStore = useDisplayStore()
const {
  panoramaViewShown,
} = storeToRefs(displayStore)
const panoramaStore = usePanoramaStore()
const {
  scene,
} = storeToRefs(panoramaStore)
const dataStore = useDataStore()
const {
  features,
} = storeToRefs(dataStore)

// setup init data
lockView.value = props.displayOptions.lockView
canEdit.value = !!props.displayOptions.canEdit
isEditMode.value = !!props.displayOptions.isEditMode
editPointId.value = props.displayOptions.editPointId
features.value = props.features

if (displaySettingStore.isOverheadViewLocked()) {
  panoramaViewShown.value = false
} else if (displaySettingStore.isPanoramaViewLocked()) {
  panoramaViewShown.value = true
  scene.value = lockView.value
}
const enableMap = computed(() => !displaySettingStore.isViewLocked() || displaySettingStore.isOverheadViewLocked())
const displayMap = computed(() => panoramaViewShown.value ? 'd-none' : 'd-block')
</script>

<template>
  <div class="app-wrapper" data-bs-theme="dark">
    <GardenMap v-if="enableMap" :class="displayMap"></GardenMap>
    <PanoramaView v-if="panoramaViewShown"></PanoramaView>
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

  &:deep() {
    @import 'bootstrap/scss/bootstrap.scss';

    .modal {
      --bs-modal-zindex: 1100;
    }
  }
}
</style>
