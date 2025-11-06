<script setup>
import { storeToRefs } from 'pinia'
import { useDataStore } from '../stores/data.js'
import { useDisplayStore } from '../stores/display.js'
import Main from './menu/Main.vue'
import History from './menu/History.vue'
import IndianResidentialSchoolsMap from './menu/IndianResidentialSchoolsMap.vue'
import ContextualEthicalFraming from './menu/ContextualEthicalFraming.vue'
import RelationalInterconnectedTeachings from './menu/RelationalInterconnectedTeachings.vue'
import FeatureList from './menu/FeatureList.vue'
import Acknowledgements from './menu/Acknowledgements.vue'
import Feature from './menu/Feature.vue'
import FeatureGallery from './menu/FeatureGallery.vue'

const dataStore = useDataStore()
const {
  plants,
  gardenFeatures,
} = storeToRefs(dataStore)
const displayStore = useDisplayStore()
const {
  menuPlantListShown,
  menuFeatureListShown,
} = storeToRefs(displayStore)
</script>

<template>
  <Main class="menu-lvl1"></Main>
  <History class="menu-lvl2 menu-wide"></History>
  <IndianResidentialSchoolsMap class="menu-lvl2 menu-wide"></IndianResidentialSchoolsMap>
  <ContextualEthicalFraming class="menu-lvl2 menu-wide"></ContextualEthicalFraming>
  <RelationalInterconnectedTeachings class="menu-lvl2 menu-wide"></RelationalInterconnectedTeachings>
  <FeatureList class="menu-lvl2" label="Plants" :items="plants" v-model:shown="menuPlantListShown"></FeatureList>
  <FeatureList class="menu-lvl2" label="Features" :items="gardenFeatures" v-model:shown="menuFeatureListShown"></FeatureList>
  <Acknowledgements class="menu-lvl2 menu-wide"></Acknowledgements>
  <Feature class="menu-lvl3 menu-wide"></Feature>
  <FeatureGallery></FeatureGallery>
</template>

<style lang="scss" scoped>
.offcanvas.menu-lvl1 {
  z-index: calc(var(--bs-offcanvas-zindex) + 11);
}
.offcanvas.menu-lvl2 {
  z-index: calc(var(--bs-offcanvas-zindex) + 21);
}
.offcanvas.menu-lvl3 {
  z-index: calc(var(--bs-offcanvas-zindex) + 31);
}
@media (min-width: 992px) {
  .offcanvas.menu-wide {
    width: 50vmax !important;
  }
}
@media (max-width: 991.98px) {
  .offcanvas.menu-wide {
    width: 100vmax !important;
  }
}
.offcanvas {
  --bs-bg-opacity: 1;
  background-color: rgba(var(--bs-tertiary-bg-rgb),var(--bs-bg-opacity)) !important;
}
.offcanvas .offcanvas-header {
  --bs-bg-opacity: 1;
  background-color: rgba(var(--bs-secondary-bg-rgb),var(--bs-bg-opacity)) !important;
}
</style>
