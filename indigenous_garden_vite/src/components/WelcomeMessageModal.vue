<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useStaticContentStore } from '../stores/data.js'
import { useDisplayStore } from '../stores/display.js'
import ContentBlock from './ContentBlock.vue'
import { _stopAllMedia, toggleModal } from '../_utils.js'
import indgLogoUrl from '../assets/INDG-RGB-reverse.png'

const {
  welcomeModalShown: shown,
} = storeToRefs(useDisplayStore())

const staticContent = await useStaticContentStore().get()
const welcomeModalContent = staticContent.welcome

const modalRef = ref(null)

watch(shown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleModal(modalRef.value, welcomeModalContent.display && newValue) }
})
onMounted(() => {
  useDisplayStore().forceShowInitialWelcomeMessage()
  toggleModal(modalRef.value, welcomeModalContent.display && shown.value)
  modalRef.value.addEventListener('hidden.bs.modal', () => {
    _stopAllMedia()
    shown.value = false
  })
  modalRef.value.addEventListener('shown.bs.modal', () => shown.value = true)
})
</script>

<template>
  <div ref="modalRef" class="modal fade" data-bs-backdrop="static" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header align-items-start">
          <div class=w-100>
            <h1 class="modal-title text-center sfu-red" v-html="welcomeModalContent.title || 'Welcome'" />
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="welcomeModalContent.content_item && welcomeModalContent.content_item.content_blocks && welcomeModalContent.content_item.content_blocks.length > 0">
            <ContentBlock v-for="contentBlock in welcomeModalContent.content_item.content_blocks" :contentBlock="contentBlock" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-lg btn-sfu-red mx-auto my-0" data-bs-dismiss="modal">{{ welcomeModalContent.close_button_label || 'Close' }}</button>
          <figure class="figure mx-auto my-0">
            <img
              class="m-0 oie-logo" :src="indgLogoUrl"
              alt="SFU Office of Indigenous Education Logo"
              loading="lazy" fetchpriority="low"
            />
          </figure>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.sfu-red {
  color: #CC0633;
}
.oie-logo {
  max-height: 53.75px;
}
.btn-sfu-red {
  --bs-btn-color: #fff;
  --bs-btn-bg: #CC0633;
  --bs-btn-border-color: #CC0633;

  /* Hover states */
  --bs-btn-hover-color: #fff;
  --bs-btn-hover-bg: #A6192E;
  --bs-btn-hover-border-color: #A6192E;

  /* Focus/Active states */
  --bs-btn-focus-shadow-rgb: 204, 6, 51;
  --bs-btn-active-color: #fff;
  --bs-btn-active-bg: #A6192E;
  --bs-btn-active-border-color: #A6192E;
}
</style>