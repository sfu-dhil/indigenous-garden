import 'vite/modulepreload-polyfill';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import OpenLayersMap from 'vue3-openlayers'
import GardenApp from './GardenApp.vue'

// include global css (boostrap modal backdrops and tooltips are in here)
import './assets/garden.scss'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const mountElList = document.querySelectorAll('#garden-app')
mountElList.forEach((mountEl) => {
  const app = createApp(GardenApp, {
    ...mountEl.dataset,
    features: JSON.parse(mountEl.dataset.featuresJson),
    displayOptions: JSON.parse(mountEl.dataset.displayOptionsJson),
  })
  app.use(pinia)
  app.use(OpenLayersMap)
  app.mount(mountEl)
})