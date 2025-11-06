import { defineStore } from 'pinia'

export const useDisplaySettingStore = defineStore('display-settings', {
  state: () => ({
    lockView: null,
    canEdit: false,
    isEditMode: false,
    editPointId: null,
  }),
  getters: {},
  actions: {
    isViewLocked() {
      return !!this.lockView
    },
    isOverheadViewLocked() {
      return this.lockView === 'overhead'
    },
    isPanoramaViewLocked() {
      return ['panorama_location_1', 'panorama_location_2', 'panorama_location_3'].includes(this.lockView)
    },
    isPanoramaLocation1ViewLocked() {
      return this.lockView === 'panorama_location_1'
    },
    isPanoramaLocation2ViewLocked() {
      return this.lockView === 'panorama_location_2'
    },
    isPanoramaLocation3ViewLocked() {
      return this.lockView === 'panorama_location_3'
    },
  },
  persist: false,
})

export const useDisplayStore = defineStore('display', {
  state: () => ({
    modalWelcomeShown: false,
    panoramaViewShown: false,

    // top level menu
    menuMainShown: false,

    // second level menus
    menuHistoryShown: false,
    menuIndianResidentialSchoolsMapShown: false,
    menuPlantListShown: false,
    menuFeatureListShown: false,
    menuAcknowledgementsShown: false,
    menuContextualEthicalFramingShown: false,
    menuRelationalInterconnectedTeachingsShown: false,

    // third level menus
    menuFeatureShown: false,
    selectedFeatureId: null,
    selectedPointId: null,
    selectedGalleryIndex: null,

    // hover feature across map/panorama
    hoverFeatureId: null,
  }),
  getters: {},
  actions: {
    forceShowInitialWelcomeMessage() {
      if (!document.cookie.split("; ").find((row) => row.startsWith("showInitialWelcomeModal"))) {
        // set cookie to expire 1 day from now
        const exp = (new Date(Date.now() + 86400e3)).toUTCString()
        document.cookie = `showInitialWelcomeModal=true; expires=${exp}; SameSite=None; Secure`
        this.modalWelcomeShown = true
      }
    },
    showMapView() {
      this.panoramaViewShown = false
    },
    showPanoramaView() {
      this.panoramaViewShown = true
    },
    showWelcomeMessage() {
      this.modalWelcomeShown = true
    },
    hideMenus() {
      this.modalWelcomeShown = false
      this.menuMainShown = false
      this.menuHistoryShown = false
      this.menuIndianResidentialSchoolsMapShown = false
      this.menuContextualEthicalFramingShown = false
      this.menuRelationalInterconnectedTeachingsShown = false
      this.menuPlantListShown = false
      this.menuFeatureListShown = false
      this.menuAcknowledgementsShown = false
      this.menuFeatureShown = false
    },
    showMainMenu() {
      this.hideMenus()
      this.menuMainShown = true
    },
    showHistory() {
      this.showMainMenu()
      this.menuHistoryShown = true
    },
    showIndianResidentialSchoolsMap() {
      this.showMainMenu()
      this.menuIndianResidentialSchoolsMapShown = true
    },
    showContextualEthicalFraming() {
      this.showMainMenu()
      this.menuContextualEthicalFramingShown = true
    },
    showRelationalInterconnectedTeachings() {
      this.showMainMenu()
      this.menuRelationalInterconnectedTeachingsShown = true
    },
    showPlantList() {
      this.showMainMenu()
      this.menuPlantListShown = true
    },
    showFeatureList() {
      this.showMainMenu()
      this.menuFeatureListShown = true
    },
    showAcknowledgements() {
      this.showMainMenu()
      this.menuAcknowledgementsShown = true
    },
    showFeature(featureId, pointId = null) {
      this.menuFeatureShown = true
      this.selectedFeatureId = featureId
      this.selectedPointId = pointId
    },
  },
  persist: {
    storage: sessionStorage,
  },
})

