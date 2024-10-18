<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore, useDisplaySetting } from '../stores/display.js'
import { loremIpsum } from 'lorem-ipsum'
import { toggleModal } from '../helpers/utils.js'

const store = useDisplayStore()
const {
  modalWelcomeShown,
} = storeToRefs(store)
const {
  canEdit,
} = useDisplaySetting()

const modalEl = useTemplateRef('welcome-modal')

watch(modalWelcomeShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleModal(modalEl.value, newValue) }
})
onMounted(() => {
  if (canEdit) {
    modalWelcomeShown.value = false
  } else {
    store.forceShowInitialWelcomeMessage()
    toggleModal(modalEl.value, modalWelcomeShown.value)
  }
  modalEl.value.addEventListener('hidden.bs.modal', () => modalWelcomeShown.value = false)
  modalEl.value.addEventListener('shown.bs.modal', () => modalWelcomeShown.value = true)
})
</script>

<template>
  <div ref="welcome-modal" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header align-items-start">
          <div class=w-100>
            <h1 class="modal-title text-center">Welcome to This Garden</h1>
            <div class="row">
              <div class="col-6 text-center first-nations-unicode click-audio-player" data-src="{{ '' }}">
                hən̓q̓əmin̓əm̓ <i class="bi bi-volume-up-fill"></i> (no audio yet)
              </div>
              <div class="col-6 text-center first-nations-unicode click-audio-player" data-src="{{ '' }}">
                Sḵwx̱wú7mesh Sníchim <i class=" bi bi-volume-up-fill"></i> (no audio yet)
              </div>
            </div>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <figure class="figure w-100">
            <svg class="figure-img w-100 object-fit-contain m-0" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
              <title>Placeholder</title>
              <rect width="100%" height="100%" fill="#20c997"></rect>
              <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image Placeholder</text>
            </svg>
            <figcaption class="figure-caption text-center">
              Image Placeholder
            </figcaption>
          </figure>

          <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
          <p>{{ loremIpsum({count: 1, units: 'paragraph'}) }}</p>
        </div>
        <div class="modal-footer">
          <button data-bs-dismiss="modal" @click="store.showHistory()" class="btn btn-primary ms-auto">
            History
          </button>
          <button data-bs-dismiss="modal" @click="store.showIndianResidentialSchoolsMap()" class="btn btn-primary">
            Indian Residential Schools Map
          </button>
          <button type="button" class="btn btn-secondary me-auto" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
</style>