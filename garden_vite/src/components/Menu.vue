<script setup>
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../stores/display.js'
import Main from './menu/Main.vue'
import History from './menu/History.vue'
import IndianResidentialSchoolsMap from './menu/IndianResidentialSchoolsMap.vue'
import FeatureList from './menu/FeatureList.vue'
import References from './menu/References.vue'
import Feature from './menu/Feature.vue'
import FeatureGallery from './menu/FeatureGallery.vue'

const store = useDisplayStore()
const {
  plants,
  features,
  menuPlantListShown,
  menuFeatureListShown,
} = storeToRefs(store)
</script>

<template>
  <Main class="menu-lvl1"></Main>
  <History class="menu-lvl2 menu-wide"></History>
  <IndianResidentialSchoolsMap class="menu-lvl2 menu-wide"></IndianResidentialSchoolsMap>
  <FeatureList class="menu-lvl2" label="Plants" :items="plants" v-model:shown="menuPlantListShown"></FeatureList>
  <FeatureList class="menu-lvl2" label="Features" :items="features" v-model:shown="menuFeatureListShown"></FeatureList>
  <References class="menu-lvl2 menu-wide"></References>
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
