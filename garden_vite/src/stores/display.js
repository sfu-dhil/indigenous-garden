import { defineStore } from 'pinia'
import { useData } from './data'

const {
  featureMap,
} = useData()
const {
  canEdit,
  isEditMode,
  editPointId,
} = JSON.parse(document.getElementById('garden-display-options').textContent)

export const useDisplaySetting = () => {
  return {
    canEdit: !!canEdit,
    isEditMode: !!isEditMode,
    editPointId,
  }
}

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
  getters: {
    plants: () => [...featureMap.values()].filter((o) => o.feature_type == 'PLANT').sort((a, b) => a.number - b.number),
    features: () => [...featureMap.values()].filter((o) => o.feature_type == 'GARDEN_FEATURE').sort((a, b) => a.number - b.number),
  },
  actions: {
    forceShowInitialWelcomeMessage() {
      if (!document.cookie.split("; ").find((row) => row.startsWith("showInitialWelcomeModal"))) {
        // set cookie to expire 1 day from now
        const exp = (new Date(Date.now() + 86400e3)).toUTCString();
        document.cookie = `showInitialWelcomeModal=true; expires=${exp}; SameSite=None; Secure`;
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
  persist: true,
})

