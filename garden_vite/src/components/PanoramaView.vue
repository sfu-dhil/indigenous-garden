

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDataStore } from '../stores/data'
import { usePanoramaStore } from '../stores/panorama.js'
import { useDisplayStore, useDisplaySettingStore } from '../stores/display.js'
import Pannellum from './Pannellum.vue'

const panoramaStore = usePanoramaStore()
const {
  scene,
  hfov,
  yaw,
  pitch,
  location1Points,
  location2Points,
  location3Points,
} = storeToRefs(panoramaStore)

const displayStore = useDisplayStore()
const {
  hoverFeatureId,
} = storeToRefs(displayStore)
const displaySettingStore = useDisplaySettingStore()
const {
  isEditMode,
} = storeToRefs(displaySettingStore)

const viewer = ref(null)

const generateHotSpot = (point) => {
  const hotSpot = {
    pitch: point.pitch,
    yaw: point.yaw,
    type: 'info',
    createTooltipFunc: hotSpotTooltip,
    createTooltipArgs: { featureId: point.featureId, pointId: point.id },
    draggable: false,
    cssClass: 'view-hotspot',
  }
  if (!isEditMode.value) {
    hotSpot.clickHandlerArgs = { featureId: point.featureId, pointId: point.id }
    hotSpot.clickHandlerFunc = (event, { featureId, pointId }) => displayStore.showFeature(featureId, pointId)
  }
  return hotSpot
}
const hotSpotEditTooltip = (hotSpotDiv) => {
  hotSpotDiv.innerHTML = `
    <div class="hot-spot-wrapper hot-spot-edit">
      <i class="fa-solid fa-location-pin"></i>
    </div>
  `
}
const hotSpotTooltip = (hotSpotDiv, {featureId, pointId}) => {
  const feature = useDataStore().getFeature(featureId)
  hotSpotDiv.innerHTML = `
    <div class="hot-spot-wrapper hot-spot" data-feature-id="${feature.id}">
      <i class="fa-solid fa-location-pin" style="color: #7cb341"></i>
      <span class="number-label">${feature.number}</span>
    </div>
  `
  hotSpotDiv.addEventListener('mouseover', () => hoverFeatureId.value = feature.id)
  hotSpotDiv.addEventListener('mouseout', () => hoverFeatureId.value = null)
}

const preview = `/static/images/panorama_${scene.value}_thumbnail.jpg`
const location1Scene = {
  title: 'Fire Pit',
  type: 'multires',
  multiRes: {
    basePath: '/static/images/panorama_location_1',
    shtHash: "5L~qx]ae%Maej[j[fQfQayM{j[ayfQayWBj[WVa|fQj[j[offQoffRj[ofj[j[j[j[fQj[fQfQ",
    path: '/%l/%s%y_%x',
    fallbackPath: '/fallback/%s',
    extension: 'jpg',
    tileResolution: 512,
    maxLevel: 4,
    cubeResolution: 2440,
  },
  yaw: 180,
  pitch: 0,
  hotSpots: location1Points.value.map((point) => generateHotSpot(point)),
}
const location2Scene = {
  type: 'multires',
  multiRes: {
    basePath: '/static/images/panorama_location_2',
    shtHash: '5J~q%Nj?xuWBWBWBWBWBofWBWBofofj[ofj[ofofj[j[WBM{aeWVWBayofayj[fQayWBayj[j[',
    path: '/%l/%s%y_%x',
    fallbackPath: '/fallback/%s',
    extension: 'jpg',
    tileResolution: 512,
    maxLevel: 4,
    cubeResolution: 2440,
  },
  yaw: 0,
  pitch: 0,
  hotSpots: location2Points.value.map((point) => generateHotSpot(point)),
}
const location3Scene = {
  type: 'multires',
  multiRes: {
    basePath: '/static/images/panorama_location_3',
    shtHash: '5K~q%Mt7xut7ofWBj[ofayRjR%ayayofofj[WBaykCj[azj[WBofayj[ofayofj[ayWBofj[WB',
    path: '/%l/%s%y_%x',
    fallbackPath: '/fallback/%s',
    extension: 'jpg',
    tileResolution: 512,
    maxLevel: 4,
    cubeResolution: 2440,
  },
  yaw: 0,
  pitch: 0,
  hotSpots: location3Points.value.map((point) => generateHotSpot(point)),
}
if (!displaySettingStore.isViewLocked()) {
  location1Scene.hotSpots.push({ type: 'scene', yaw: -165.81727582264662, pitch: 1.113782204857499, sceneId: 'panorama_location_2', text: 'Jump to location' })
  location1Scene.hotSpots.push({ type: 'scene', yaw: 133.99728303521908, pitch: 1.113782204857499, sceneId: 'panorama_location_3', text: 'Jump to location' })
  location2Scene.hotSpots.push({ type: 'scene', yaw: 108.90797032638226, pitch: -16.892185445760447, sceneId: 'panorama_location_1', text: 'Jump to Fire Pit' })
  location2Scene.hotSpots.push({ type: 'scene', yaw: 178.04711595546553, pitch: -12.005839879584766, sceneId: 'panorama_location_3', text: 'Jump to location' })
  location3Scene.hotSpots.push({ type: 'scene', yaw: 155.36307243810427, pitch: -19.856401239086544, sceneId: 'panorama_location_1', text: 'Jump to Fire Pit' })
  location3Scene.hotSpots.push({ type: 'scene', yaw: 95.54536960098842, pitch: -7.897351828203455, sceneId: 'panorama_location_2', text: 'Jump to location' })
}
const pannellumSrc = {
  default: { firstScene: scene.value },
  scenes: {
    panorama_location_1: location1Scene,
    panorama_location_2: location2Scene,
    panorama_location_3: location3Scene,
  }
}
const zoomIn = () => hfov.value = hfov.value - 10
const zoomOut = () => hfov.value = hfov.value + 10

watch(hoverFeatureId, (newValue, oldValue) => {
  if (newValue != oldValue) {
    document.querySelectorAll('.hot-spot').forEach( (domEl) => {
      domEl.dataset.featureId && domEl.dataset.featureId === `${newValue}` ? domEl.classList.add('hover') : domEl.classList.remove('hover')
    })
  }
})

onMounted(() => {
  hoverFeatureId.value = null

  if (viewer.value) {
    viewer.value.on('scenechange', (newScene) => scene.value = newScene)
    if (isEditMode.value) {
      const editInitialPitch = panoramaStore.getEditInitialPitch()
      const editInitialYaw = panoramaStore.getEditInitialYaw()
      const addNewHotSpot = ([pitch, yaw]) => {
        viewer.value.addHotSpot({
          pitch,
          yaw,
          type: 'info',
          draggable: true,
          dragHandlerFunc: (event) => {
            if (["mouseup", "touchend", "pointerup"].includes(event.type)) {
              const [pitch, yaw] = viewer.value.mouseEventToCoords(event)
              panoramaStore.updateEditForm(yaw, pitch)
            }
          },
          cssClass: 'edit-hotspot',
          createTooltipFunc: hotSpotEditTooltip,
        }, scene.value)
        panoramaStore.updateEditForm(yaw, pitch)
      }

      // if coordinates already exist (editing point, or form pitch/yaw already set (ex: page reload))
      if (editInitialPitch && editInitialYaw) {
        pitch.value = editInitialPitch
        yaw.value = editInitialYaw
        addNewHotSpot([editInitialPitch, editInitialYaw])
      } else {
        // add click event to add new point at click location
        const addNewHotSpotClick = (event) => {
            addNewHotSpot(viewer.value.mouseEventToCoords(event));
            // remove click event
            viewer.value.off('mouseup', addNewHotSpotClick);
        }
        viewer.value.on('mouseup', addNewHotSpotClick)
      }
    }
  }
})
</script>

<template>
  <div class="w-100 h-100 position-absolute">
    <div class="ol-zoom ol-unselectable ol-control text-secondary">
      <button @click="zoomIn" type="button" class="ol-zoom-in" title="Zoom in">+</button>
      <button @click="zoomOut" type="button" class="ol-zoom-out" title="Zoom out">–</button>
    </div>
    <div v-if="!isEditMode" class="show-menu-control ol-unselectable ol-control text-secondary">
      <button @click="() => displayStore.showMainMenu()" type="button" title="Show Menu">
        <i class="bi bi-list-ol"></i>
      </button>
    </div>
    <div v-if="!isEditMode" class="show-welcome-control ol-unselectable ol-control text-secondary">
      <button @click="() => displayStore.showWelcomeMessage()" type="button" title="Show Welcome Message">
        <i class="fa-solid fa-message"></i>
      </button>
    </div>
    <div v-if="!displaySettingStore.isViewLocked()" class="select-view-control ol-unselectable ol-control text-secondary">
      <button type="button" @click="() => displayStore.showMapView()" title="Panorama view. Click to switch to Map view">
        <i class="bi bi-pin-map-fill"></i>
      </button>
    </div>
    <Pannellum
      id="pannellum-view"
      v-model:viewer="viewer" v-model:src="pannellumSrc"
      v-model:hfov="hfov" v-model:yaw="yaw" v-model:pitch="pitch"
      :preview="preview" :autoLoad="true"
      :draggable="true" :showControls="false" :compass="false"
      class="w-100 h-100"
    ></Pannellum>
  </div>
</template>

<style lang="scss" scoped>
.ol-control  {
  z-index: 100 !important;
  pointer-events: auto;
}
.ol-control button {
  font-size: 1.5em !important;
  pointer-events: auto;
  i {
      cursor: pointer;
    }
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
.view-hotspot .hot-spot-wrapper.hover i  {
    --bs-border-opacity: 1;
    -webkit-text-stroke-color: rgba(var(--bs-primary-rgb),var(--bs-border-opacity)) !important;
}

#pannellum-view:deep() {
  /* these do not hide properly in tour mode */
  .pnlm-panorama-info,
  .pnlm-zoom-controls,
  .pnlm-fullscreen-toggle-button {
    display: none;
    visibility: hidden;
  }

  .hot-spot-wrapper {
    font-size: 16pm;
    font-weight: bold;
    position: relative;
  }
  .hot-spot-wrapper .number-label {
    color: white;
    font-size: 0.7em;
    z-index: 1001;
    position: absolute;
    left: 0;
    right: 0;
    bottom: calc(50% - 0.35em);
    text-align: center;
  }

  .hot-spot-wrapper i {
    font-size: 1.6em;
    z-index: 1000;
  }

  .view-hotspot .hot-spot-wrapper i,
  .edit-hotspot .hot-spot-wrapper i {
    -webkit-text-stroke-width: 2px;
    -webkit-text-stroke-color: white;
  }

  .view-hotspot .hot-spot-wrapper.hover i  {
      --bs-border-opacity: 1;
      -webkit-text-stroke-color: rgba(var(--bs-primary-rgb),var(--bs-border-opacity)) !important;
  }

  .edit-hotspot .hot-spot-wrapper {
      cursor: pointer;
      color: red;
  }

  .edit-hotspot .hot-spot-wrapper:hover::after {
      content: "\F287";
      font-family: bootstrap-icons !important;
      font-size: 0.6em;
      position: absolute;
      bottom: -0.3em;
      left: 0;
      right: 0;
      text-align: center;
      color: rgb(0, 153, 255);
      -webkit-text-stroke-width: 1px;
      -webkit-text-stroke-color: black;
  }
}
</style>