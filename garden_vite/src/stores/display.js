import { defineStore } from 'pinia'

export const useDisplaySettingStore = defineStore('display-settings', {
  state: () => ({
    canEdit: false,
    isEditMode: false,
    editPointId: null,
  }),
  getters: {},
  actions: {},
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
    menuReferencesShown: false,

    // third level menus
    menuFeatureShown: false,
    selectedFeatureId: null,
    selectedPointId: null,
    selectedGalleryIndex: null,
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
      this.menuPlantListShown = false
      this.menuFeatureListShown = false
      this.menuReferencesShown = false
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
    showPlantList() {
      this.showMainMenu()
      this.menuPlantListShown = true
    },
    showFeatureList() {
      this.showMainMenu()
      this.menuFeatureListShown = true
    },
    showReferences() {
      this.showMainMenu()
      this.menuReferencesShown = true
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

