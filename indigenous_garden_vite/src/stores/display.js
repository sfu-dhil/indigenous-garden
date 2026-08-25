import { defineStore } from 'pinia'
import { getCenter, boundingExtent } from 'ol/extent'
import { _stopAllMedia } from '../_utils.js'
import { MapResourceTypes } from '../_resourceTypes.js'

export const useDisplayOpenlayersStore = defineStore('display-openlayers', {
  state: () => ({
    baseUnboundExtent: null,
    extent: null,
    center: null,
    zoom: null,
    rotation: null,
  }),
  getters: {},
  actions: {
    reset () {
      this.baseUnboundExtent = null
      this.extent = null
      this.center = null
      this.zoom = null
      this.rotation = null
    },
    init (map) {
      if (map && [MapResourceTypes.overheadImageMap, MapResourceTypes.xyzMap].includes(map.resourcetype)) {
        this.baseUnboundExtent = undefined
        this.extent = map.properties?.bounding_box ? boundingExtent(map.properties?.bounding_box.flat()) : undefined
        if (map.resourcetype === MapResourceTypes.overheadImageMap) {
          this.baseUnboundExtent = [0, -map.height, map.width, 0]
          if (this.extent === undefined) {
            this.extent = this.baseUnboundExtent
          }
        }
        // defaults
        this.center = this.extent ? getCenter(this.extent) : [0, 0]
        this.zoom = map.min_zoom && map.max_zoom ? (map.max_zoom - map.min_zoom) / 2 : 1
        this.rotation = 0
        // optional initial value overrides
        if (map.properties?.initial) {
          this.center = map.properties.initial.center
          this.zoom = map.properties.initial.zoom
          this.rotation = map.properties.initial.rotation
        }
      } else {
        this.reset()
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})

export const useDisplayPannellumStore = defineStore('display-pannellum', {
  state: () => ({
    hfov: null,
    yaw: null,
    pitch: null,
  }),
  getters: {},
  actions: {
    reset () {
      this.hfov = null
      this.yaw = null
      this.pitch = null
    },
    init (map) {
      if (map && [MapResourceTypes.panoramaImageMap].includes(map.resourcetype)) {
        // defaults
        this.hfov = 100
        this.yaw = 0
        this.pitch = 0
        // optional initial value overrides
        if (map.properties?.initial) {
          this.hfov = map.properties.initial.hfov
          this.yaw = map.properties.initial.yaw
          this.pitch = map.properties.initial.pitch
        }
      } else {
        this.reset()
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})

export const useDisplayImageModalStore = defineStore('display-image-modal', {
  state: () => ({
    shown: false,
    object: null,
  }),
  getters: {},
  actions: {
    showImage (object) {
      this.object = object
      this.shown = true
    },
  },
})

export const useDisplayImageGalleryModalStore = defineStore('display-image-gallery-modal', {
  state: () => ({
    shown: false,
    objects: [],
    galleryIndex: null,
  }),
  getters: {},
  actions: {
    showGalleryImage (galleryIndex, objects) {
      this.objects = objects
      this.shown = true
      this.galleryIndex = galleryIndex
    },
  },
})


export const FeatureFilterTypes = Object.freeze({
  plant: 'plant',
  gardenFeature: 'garden_feature',
})

export const useDisplayStore = defineStore('display', {
  state: () => ({
    welcomeModalShown: false,
    mapSelectSidebarShown: false,
    infoPageIdShown: null,
    menuSidebarShown: false,
    featureIdHover: null,
    featureIdShown: null,
    featureSelectionSidebarShown: false,
    featureSelectionSidebarFilterType: null,
  }),
  getters: {},
  actions: {
    forceShowInitialWelcomeMessage() {
      // if (!document.cookie.split("; ").find((row) => row.startsWith("showInitialWelcomeModal"))) {
      //   // set cookie to expire 1 day from now
      //   const exp = (new Date(Date.now() + 86400e3)).toUTCString()
      //   document.cookie = `showInitialWelcomeModal=true; expires=${exp}; SameSite=None; Secure`
      //   this.welcomeModalShown = true
      // }
      this.welcomeModalShown = true
    },
    showInfoPage(infoPage) {
      this.infoPageIdShown = infoPage.id
    },
    showFeature(feature) {
      this.featureIdShown = feature.id
    },
    hideSidebars() {
      this.menuSidebarShown = false
      this.featureSelectionSidebarShown = false
      this.mapSelectSidebarShown = false
      this.featureSelectionSidebarFilterType = null
    },
    showMapSelectSidebar() {
      this.hideSidebars()
      this.mapSelectSidebarShown = true
    },
    showMenuSidebar() {
      this.hideSidebars()
      this.menuSidebarShown = true
    },
    showFeatureSelectionSidebar(filterType) {
      // this.hideSidebars()
      this.featureSelectionSidebarShown = true
      this.featureSelectionSidebarFilterType = filterType
    },
  },
  persist: {
    storage: sessionStorage,
  },
})

const audioPlayer = new Audio()
audioPlayer.preload = 'none'
export const useAudioLabelMediaStore = defineStore('audio-label-media', {
  state: () => ({
    currentAudio: null,
  }),
  getters: {},
  actions: {
    stopAudio() {
      this.currentAudio = null
      audioPlayer.removeEventListener('ended', this.stopAudio)
      audioPlayer.removeEventListener('pause', this.stopAudio)
      if (audioPlayer.src) {
        audioPlayer.pause()
        audioPlayer.currentTime = 0
      }
    },
    toggleAudio(audio) {
      if (this.currentAudio === audio) {
        this.stopAudio()
      } else {
        _stopAllMedia()
        this.currentAudio = audio
        audioPlayer.src = audio
        audioPlayer.play()
        audioPlayer.addEventListener('ended', this.stopAudio)
        audioPlayer.addEventListener('pause', this.stopAudio)
      }
    },
  },
  persist: false,
})
