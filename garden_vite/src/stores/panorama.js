import { defineStore } from 'pinia'
import { useDataStore } from './data'
import { useDisplaySettingStore } from './display'

export const usePanoramaStore = defineStore('panorama', {
  state: () => ({
    scene: 'panorama_location_1',
    hfov: 100,
    yaw: 180,
    pitch: 0,
  }),
  getters: {
    location1Points: () => useDataStore().location1Points.sort((a, b) => b.pitch - a.pitch || a.yaw -  b.yaw).filter((o) => !useDisplaySettingStore().isEditMode || (useDisplaySettingStore().lockView === 'panorama_location_1' && o.id !== useDisplaySettingStore().editPointId)),
    location2Points: () => useDataStore().location2Points.sort((a, b) => b.pitch - a.pitch || a.yaw -  b.yaw).filter((o) => !useDisplaySettingStore().isEditMode || (useDisplaySettingStore().lockView === 'panorama_location_2' && o.id !== useDisplaySettingStore().editPointId)),
    location3Points: () => useDataStore().location3Points.sort((a, b) => b.pitch - a.pitch || a.yaw -  b.yaw).filter((o) => !useDisplaySettingStore().isEditMode || (useDisplaySettingStore().lockView === 'panorama_location_3' && o.id !== useDisplaySettingStore().editPointId)),
    editPoint: () => {
      if (useDisplaySettingStore().isPanoramaLocation1ViewLocked()) {
        return useDataStore().location1Points.find((o) => o.id === useDisplaySettingStore().editPointId)
      } else if (useDisplaySettingStore().isPanoramaLocation2ViewLocked()) {
        return useDataStore().location2Points.find((o) => o.id === useDisplaySettingStore().editPointId)
      } else if (useDisplaySettingStore().isPanoramaLocation3ViewLocked()) {
        return useDataStore().location3Points.find((o) => o.id === useDisplaySettingStore().editPointId)
      }
      return null
    },
  },
  actions: {
    getEditInitialYaw () {
      if (document.getElementById("id_yaw")?.value && !isNaN(parseFloat(document.getElementById("id_yaw").value))) { return parseFloat(document.getElementById("id_yaw").value) }
      if (this.editPoint?.yaw) { return this.editPoint.yaw }
      return null
    },
    getEditInitialPitch () {
      if (document.getElementById("id_pitch")?.value && !isNaN(parseFloat(document.getElementById("id_pitch").value))) { return parseFloat(document.getElementById("id_pitch").value) }
      if (this.editPoint?.pitch) { return this.editPoint.pitch }
      return null
    },
    updateEditForm (yaw, pitch) {
      if (document.getElementById("id_yaw")) { document.getElementById("id_yaw").value = `${yaw}` }
      if (document.getElementById("id_pitch")) { document.getElementById("id_pitch").value = `${pitch}` }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})
