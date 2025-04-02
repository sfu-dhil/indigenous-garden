import { defineStore } from 'pinia'
import { useDataStore } from './data'
import { useDisplaySettingStore } from './display'
import { getCenter } from 'ol/extent'
import { TileGrid } from 'ol/tilegrid'


const DEFAULT_ROTATION = 0
// const NORTH_ROTATION = (15.0 * Math.PI) / 180.0
const IMAGE_WIDTH = 3840
const IMAGE_HEIGHT = 2160
const IMAGE_EXTENT = [0, -IMAGE_HEIGHT, IMAGE_WIDTH, 0]
const PROJECTION = {
  units: "pixels",
  extent: IMAGE_EXTENT,
}
const TILE_GRID = new TileGrid({
  extent: IMAGE_EXTENT,
  origin: [0, 0],
  resolutions: [32, 16, 8, 4, 2, 1],
  tileSize: [128, 128],
})

export const useMapStore = defineStore('map', {
  state: () => ({
    center: getCenter(IMAGE_EXTENT),
    zoom: 2.5,
    rotation: DEFAULT_ROTATION,
  }),
  getters: {
    points: () => useDataStore().points.sort((a, b) => b.y - a.y || a.x -  b.x).filter((o) => !useDisplaySettingStore().isEditMode || o.id !== useDisplaySettingStore().editPointId),
    editPoint: () => useDataStore().points.find((o) => o.id === useDisplaySettingStore().editPointId),
    projection: () => PROJECTION,
    imageExtent: () => IMAGE_EXTENT,
    defaultRotation: () => DEFAULT_ROTATION,
    tileGrid: () => TILE_GRID,
  },
  actions: {
    getEditInitialX () {
      if (this.editPoint?.x) { return this.editPoint.x }
      if (document.getElementById("id_x")?.value) { return parseFloat(document.getElementById("id_x").value) }
      return null
    },
    getEditInitialY () {
      if (this.editPoint?.y) { return this.editPoint.y }
      if (document.getElementById("id_y")?.value) { return parseFloat(document.getElementById("id_y").value) }
      return null
    }
  },
  persist: {
    storage: sessionStorage,
  },
})
