import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', {
  state: () => ({
    features: [],
  }),
  getters: {
    featuresMap: (state) => state.features.reduce((result, o) => result.set(o.id, o), new Map()),
    points: (state) => state.features.reduce((result, o) => result.concat(o.points.map((p) => ({...p, featureId: o.id}))), []),
    location1Points: (state) => state.features.reduce((result, o) => result.concat(o.location_1_panorama_points.map((p) => ({...p, featureId: o.id}))), []),
    location2Points: (state) => state.features.reduce((result, o) => result.concat(o.location_2_panorama_points.map((p) => ({...p, featureId: o.id}))), []),
    location3Points: (state) => state.features.reduce((result, o) => result.concat(o.location_3_panorama_points.map((p) => ({...p, featureId: o.id}))), []),
    plants: (state) => state.features.filter((o) => o.feature_type == 'PLANT').sort((a, b) => a.number - b.number),
    gardenFeatures: (state) => state.features.filter((o) => o.feature_type == 'GARDEN_FEATURE').sort((a, b) => a.number - b.number),
  },
  actions: {
    getFeature(id) {
      return this.featuresMap.has(id) ? this.featuresMap.get(id) : null
    },
  },
  persist: false,
})
