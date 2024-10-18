import 'vite/modulepreload-polyfill';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import OpenLayersMap from 'vue3-openlayers'
import GardenApp from './GardenApp.vue'

// include global css (boostrap modal backdrops and tooltips are in here)
import './assets/garden.scss'

// disable warnings (mostly from `videojs-vr`'s `three.js`)
console.warn = () => {};

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(GardenApp)
app.use(pinia)
app.use(OpenLayersMap)
app.mount('#garden-app')