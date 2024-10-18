import { defineStore } from 'pinia'
import { useData } from './data'
import { useDisplaySetting } from './display'
import { getCenter } from 'ol/extent'

const NORTH_ROTATION = (15.0 * Math.PI) / 180.0
const IMAGE_WIDTH = 2050
const IMAGE_HEIGHT = 1510
const imageExtent = [0, -IMAGE_HEIGHT, IMAGE_WIDTH, 0]
const projection = {
  units: "pixels",
  extent: imageExtent,
}

const {
  points,
} = useData()
const {
  isEditMode,
  editPointId,
} = useDisplaySetting()

export const useMapStore = defineStore('map', {
  state: () => ({
    center: getCenter(imageExtent),
    zoom: 2.5,
    rotation: NORTH_ROTATION,
    hoverId: null,
  }),
  getters: {
    points: () => points.sort((a, b) => b.y - a.y || a.x -  b.x).filter((o) => !isEditMode || o.id !== editPointId),
    editPoint: () => points.find((o) => o.id === editPointId),
    projection: () => projection,
    imageExtent: () => imageExtent,
    defaultRotation: () => NORTH_ROTATION,
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
  persist: true,
})
