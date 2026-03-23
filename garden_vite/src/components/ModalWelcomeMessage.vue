<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useDisplaySettingStore, useInterfaceContentStore } from '../stores/display.js'
import { useMediaStore } from '../stores/media.js'
import { toggleModal } from '../helpers/utils.js'
import DisplayName from './DisplayName.vue'

const displayStore = useDisplayStore()
const {
  modalWelcomeShown,
} = storeToRefs(displayStore)
const displaySettingStore = useDisplaySettingStore()
const {
  canEdit,
} = storeToRefs(displaySettingStore)
const interfaceContentStore = useInterfaceContentStore()
const {
  welcomePopupContent,
} = storeToRefs(interfaceContentStore)

const modalEl = useTemplateRef('welcome-modal')

watch(modalWelcomeShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleModal(modalEl.value, newValue) }
})
onMounted(() => {
  if (canEdit.value) {
    modalWelcomeShown.value = false
  } else {
    displayStore.forceShowInitialWelcomeMessage()
    toggleModal(modalEl.value, modalWelcomeShown.value)
  }
  modalEl.value.addEventListener('hidden.bs.modal', () => {
    useMediaStore().stopAllMedia()
    modalWelcomeShown.value = false
  })
  modalEl.value.addEventListener('shown.bs.modal', () => modalWelcomeShown.value = true)
})
</script>

<template>
  <div ref="welcome-modal" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header align-items-start">
          <div class=w-100>
            <h1 class="modal-title text-center" v-html="welcomePopupContent.heading" />
            <div class="row">
              <div class="col-6 text-center first-nations-unicode">
                <DisplayName v-if="welcomePopupContent.heading_halkomelem" :item="{name: welcomePopupContent.heading_halkomelem, audio: welcomePopupContent.heading_halkomelem_audio}" :withAudio="true" />
              </div>
              <div class="col-6 text-center first-nations-unicode">
                <DisplayName v-if="welcomePopupContent.heading_squamish" :item="{name: welcomePopupContent.heading_squamish, audio: welcomePopupContent.heading_squamish_audio}" :withAudio="true" />
              </div>
            </div>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <figure class="figure w-100" v-if="welcomePopupContent.image && welcomePopupContent.thumbnail">
            <img class="figure-img w-100 object-fit-contain m-0"
                  loading="lazy" fetchpriority="low"
                  :alt="welcomePopupContent.image_caption"
                  :src="welcomePopupContent.thumbnail">
            <figcaption class="figure-caption text-center" v-if="welcomePopupContent.image_caption" v-html="welcomePopupContent.image_caption" />
          </figure>
          <div v-if="welcomePopupContent.content" v-html="welcomePopupContent.content" />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary mx-auto" data-bs-dismiss="modal">Step into the Garden</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
</style>