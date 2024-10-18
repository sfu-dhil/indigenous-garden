

<script setup>
import { ref, inject, onMounted, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { Style, Text, Fill, Stroke } from "ol/style"
import { easeOut } from "ol/easing"
import { Collection } from 'ol'
import { useData } from '../stores/data.js'
import { useMapStore } from '../stores/map.js'
import { useDisplayStore, useDisplaySetting } from '../stores/display.js'


const {
  featureMap,
} = useData()
const store = useMapStore()
const {
  center,
  rotation,
  zoom,
} = store
const {
  points,
  projection,
  hoverId,
  defaultRotation,
} = storeToRefs(store)
const displayStore = useDisplayStore()
const {
  isEditMode,
} = useDisplaySetting()

const mapRef = ref(null)
const editFeatureRef = ref(null)
const editFeatures = ref(new Collection())
const editInitialX = ref(store.getEditInitialX())
const editInitialY = ref(store.getEditInitialY())

const overrideEditFeatureStyle = (openLayersFeature) => {
  return [
    new Style({
      text: new Text({
        text: '\uf041',
        scale: 1.6,
        textBaseline: 'bottom',
        font: 'bold 16px "Font Awesome 6 Free"',
        fill: new Fill({ color: 'red' }),
        stroke: new Stroke({ color: 'white', width: 3 }),
      }),
      zIndex: Infinity,
    }),
  ]
}
const overrideFeatureStyle = (openLayersFeature) => {
  const featureId = openLayersFeature.get('featureId')
  const feature = featureMap.get(featureId)
  const fillColor = feature.feature_type == 'FEATURE' ? '#6495ED' : '#7cb341'
  return [
    new Style({
      text: new Text({
        text: '\uf041',
        scale: 1.6,
        textBaseline: 'bottom',
        font: 'bold 1em "Font Awesome 6 Free"',
        fill: new Fill({ color: fillColor }),
        stroke: new Stroke({ color: 'white', width: 3 }),
      }),
    }),
    new Style({
      text: new Text({
        text: `${feature.number}`,
        scale: 0.8,
        textBaseline: 'bottom',
        font: 'bold 1em "BC Sans"',
        // offsetX: `${number}`.length - 1,
        offsetY: -8,
        fill: new Fill({ color: 'white' }),
      }),
    }),
  ]
}
const overrideSelectedFeatureStyle = (openLayersFeature) => {
  const styles = overrideFeatureStyle(openLayersFeature)
  styles[0].text_.stroke_.color_ = [13, 110, 253, 1]
  styles[0].text_.stroke_.width_ = 3
  styles[0].zIndex_ = Infinity
  styles[1].zIndex_ = Infinity
  return styles
}

const updateCenter = (event) => store.center = event.target.getCenter()
const updateZoom = (event) => store.zoom = event.target.getZoom()
const updateRotation = (event) => store.rotation = event.target.getRotation()

const hoverFeature = (event) => {
  if (event.selected.length > 0) {
    hoverId.value = event.selected[0].get('featureId')
  } else {
    hoverId.value = null
  }
}
const clickFeature = (event) => {
  if (event.selected.length > 0) {
    const selected = event.selected[0]
    displayStore.showFeature(selected.get('featureId'), selected.get('pointId'))
  }
}
const resetNorth = () => {
  const view = mapRef.value.map.getView()
  if (view.getRotation() % (2 * Math.PI) !== defaultRotation.value) {
    view.animate({
      rotation: defaultRotation.value,
      easing: easeOut,
    })
  }
}
const rotationLabel = () => {
  const compassIcon = document.createElement('span')
  compassIcon.innerHTML = `<span class="rotation-correction">⇧</span>`
  return compassIcon
}

const updateFormCoordinates = (coordinates) => {
  document.getElementById("id_x").value = `${coordinates[0]}`
  document.getElementById("id_y").value = `${coordinates[1]}`
}
const addEditFeature = () => {
  const olFeature = editFeatureRef.value.feature
  olFeature.on('change', function() {
    updateFormCoordinates(this.getGeometry().getCoordinates())
  }, olFeature)
  editFeatures.value.push(olFeature)
}
const addNewEditFeatureClick = (event) => {
  editInitialX.value = event.coordinate[0]
  editInitialY.value = event.coordinate[1]
  updateFormCoordinates(event.coordinate)
  mapRef.value.map.un('click', addNewEditFeatureClick)
  nextTick(() => addEditFeature())
}
onMounted(() => {
  if (isEditMode) {
    hoverId.value = null
    if (editInitialX.value && editInitialY.value) {
      addEditFeature()
    } else {
      mapRef.value.map.on('click', addNewEditFeatureClick)
    }
  }
})
const {
  pointerMove: pointerMoveCondition,
  click: clickCondition,
} = inject("ol-selectconditions")
</script>

<template>
  <div class="w-100 h-100 overflow-hidden">
    <ol-map
      ref="mapRef"
      id="garden-map"
      class="w-100 h-100 position-absolute"
      :loadTilesWhileAnimating="true"
      :loadTilesWhileInteracting="true"
      :controls="[]"
    >
      <ol-view
        :center="center"
        :rotation="rotation"
        :zoom="zoom"
        :minZoom="1"
        :maxZoom="5"
        :projection="projection"
        @change:center="updateCenter"
        @change:resolution="updateZoom"
        @change:rotation="updateRotation"
      />

      <ol-tile-layer>
        <ol-source-xyz
          :url="'/static/images/garden/{z}/{x}/{y}.webp'"
          :tileSize="[128, 128]"
          :maxResolution="32"
          :projection="projection"
        />
      </ol-tile-layer>

      <ol-vector-layer>
        <ol-source-vector>
          <ol-feature v-for="point in points" :properties="{ 'pointId': point.id, 'featureId': point.featureId }">
            <ol-geom-point :coordinates="[point.x, point.y]"></ol-geom-point>
            <ol-style :overrideStyleFunction="!isEditMode && hoverId == point.featureId ? overrideSelectedFeatureStyle : overrideFeatureStyle"></ol-style>
          </ol-feature>
          <ol-interaction-select
            v-if="!isEditMode"
            @select="hoverFeature"
            :condition="pointerMoveCondition"
          >
            <ol-style :overrideStyleFunction="overrideSelectedFeatureStyle"></ol-style>
          </ol-interaction-select>
          <ol-interaction-select
            v-if="!isEditMode"
            @select="clickFeature"
            :condition="clickCondition"
          >
            <ol-style :overrideStyleFunction="overrideSelectedFeatureStyle"></ol-style>
          </ol-interaction-select>
        </ol-source-vector>
      </ol-vector-layer>
      <ol-vector-layer v-if="isEditMode">
        <ol-source-vector>
          <ol-feature ref="editFeatureRef">
            <ol-geom-point v-if="editInitialX && editInitialY" :coordinates="[editInitialX, editInitialY]"></ol-geom-point>
            <ol-style :overrideStyleFunction="overrideEditFeatureStyle"></ol-style>
          </ol-feature>
          <ol-interaction-modify :features="editFeatures"></ol-interaction-modify>
        </ol-source-vector>
      </ol-vector-layer>

      <ol-interaction-dragrotatezoom />
      <ol-zoom-control zoomOutLabel="–" />
      <ol-rotate-control :autoHide="false" :resetNorth="resetNorth" :label="rotationLabel()" />
      <ol-toggle-control
        v-if="!isEditMode"
        className="show-menu-control"
        title="Show Menu"
        html='<i class="bi bi-list-ol"></i>'
        :onToggle="() => displayStore.showMainMenu()"
      />
      <ol-toggle-control
        v-if="!isEditMode"
        className="show-welcome-control"
        title="Show Welcome Message"
        html='<i class="fa-solid fa-door-open"></i>'
        :onToggle="() => displayStore.showWelcomeMessage()"
      />
      <ol-toggle-control
        v-if="!isEditMode"
        className="select-view-control"
        title="Map view. Click to switch to Panorama view"
        html='<i class="fa-solid fa-street-view"></i>'
        :onToggle="() => displayStore.showPanoramaView()"
      />
    </ol-map>
  </div>
</template>

<style lang="scss" scoped>
#garden-map {
  cursor: grab;
}
#garden-map:active {
  cursor: grabbing;
}
#garden-map::v-deep {
  .ol-control button {
    font-size: 1.5em;
    pointer-events: auto;
  }
  .ol-button i {
    color: inherit;
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
  .rotation-correction {
    transform: rotate(345deg);
    display: block;
  }
}
</style>