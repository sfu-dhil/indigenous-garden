import 'vite/modulepreload-polyfill'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createWebHashHistory, createRouter } from 'vue-router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VideoPlayer from '@videojs-player/vue'
import OpenLayersMap from 'vue3-openlayers'
import MapRedirectDefault from './components/MapRedirectDefault.vue'
import MapView from './components/MapView.vue'
import IndigenousGardenApp from './IndigenousGardenApp.vue'

// include global css (boostrap modal backdrops and tooltips are in here)
import './assets/indigenous-garden.scss'

// import 'videojs-contrib-quality-levels' // included in videojs-hls-quality-selector
import 'videojs-hls-quality-selector/src/plugin'
import 'videojs-theme-kit/videojs-skin.min.js'
import './_videojs-vtt-thumbnails.js'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const routes = [
  {
    path: '/',
    name: 'default',
    component: MapRedirectDefault,
  },
  {
    path: '/:id',
    name: 'map',
    component: MapView,
  },
]
const router = createRouter({
  linkActiveClass: 'active',
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return { top: 0 }
  },
})

const ready = (fn) => document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn)
ready(() => {
  document.querySelectorAll('.indigenous-garden-app').forEach((mountEl) => {
    const app = createApp(IndigenousGardenApp, { ...mountEl.dataset })
    app.use(pinia)
    app.use(OpenLayersMap)
    app.use(VideoPlayer)
    app.use(router)
    app.mount(mountEl)
  })
})