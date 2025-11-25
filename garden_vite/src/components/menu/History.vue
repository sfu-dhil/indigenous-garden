<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'
import { ImgComparisonSlider } from '@img-comparison-slider/vue';
import VideoPlayerWrapper from '../VideoPlayerWrapper.vue'

const displayStore = useDisplayStore()
const {
  menuHistoryShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuHistoryShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuHistoryShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuHistoryShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuHistoryShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">History of the SFU Indigenous Plant Garden</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" v-if="menuHistoryShown">
      <figure class="figure w-100">
        <VideoPlayerWrapper
          video="/static/videos/History_of_the_Garden/master.mpd"
          title="The Making of the Indigenous Garden"
          thumbnail="/static/thumbnails/History_of_the_Garden.png"
          thumbnails_vtt="/static/thumbnails/History_of_the_Garden/thumbnails.vtt"
        ></VideoPlayerWrapper>
        <figcaption class="figure-caption text-center">
          The Making of the Indigenous Garden
        </figcaption>
      </figure>

      <figure class="figure w-100">
        <ImgComparisonSlider class="w-100">
          <svg slot="first" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#20c997"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 1 Placeholder</text>
          </svg>
          <svg slot="second" width="100%" height="280" xmlns="http://www.w3.org/2000/svg">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#868e96"></rect>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#dee2e6">Image 2 Placeholder</text>
          </svg>
          <!-- <img slot="first" width="100%" src="images/green-leaves.0ebdd195.webp" loading="lazy" fetchpriority="low"> -->
          <!-- <img slot="second" width="100%" src="images/green-leaves-blurred.6ba79d3a.webp" loading="lazy" fetchpriority="low"> -->
        </ImgComparisonSlider>
        <figcaption class="figure-caption text-center">
          Before and after of the Indigenous Garden
        </figcaption>
      </figure>

      <p>The vision for the SFU Indigenous Plant Garden has lived in the university community for many years, carried by those who sought a place on Burnaby Mountain where Indigenous students, staff, faculty, and community members could feel grounded in identity, culture, and relationship. The garden began to take shape just before the COVID-19 pandemic, inspired by SFU’s commitments to reconciliation and the calls to action of the TRC and ARC report. It was imagined as more than a landscape project; it was meant to be a learning space where teachings, stories, and medicines could be encountered on the land rather than confined to a classroom.</p>
      <p>From the beginning, the work was guided by the host Nations — the səlilwətaɬ, kʷikʷəƛ̓əm, Sḵwx̱wú7mesh, and xʷməθkʷəy̓əm peoples — whose direction, support, and generosity informed both the spirit and the shape of the garden. A landscape designer helped develop the physical layout, and Indigenous plant ethnobotanist Cease Weiss played a central role in identifying which beings should live here. The plants chosen are important medicines for local Indigenous peoples, carrying teachings about healing, nourishment, protection, and relationship. Their presence is intentional: each plant reminds us of cultural continuity and the deep roots of Indigenous knowledge on these lands.</p>
      <p>Before any planting began, a ground awakening ceremony was held. Elders, knowledge keepers, staff, and community members gathered to acknowledge the land, offer gratitude, and ask permission. This moment set the foundation for the entire project. It affirmed that the garden is not an object or a display; it is a living relative, and the work of tending it must follow the principles of respect, reciprocity, and relational accountability.</p>
      <p>The COVID-19 pandemic brought significant delays, followed by shifts in staffing and leadership. Yet the intention of the garden remained steady. Members of the Faculty of Education, ARC committee leaders, Indigenous educators, students, and Facilities staff continued to carry the project forward. As the plants were finally placed into the earth, they were welcomed by the many hands of students, knowledge keepers, gardeners, and university staff working together to build something that honours Indigenous presence and resurgence at SFU.</p>
      <p>The garden continues to evolve. Its first years have been dedicated to establishing the health of the plants and understanding how they respond to the climate and conditions of Burnaby Mountain. Additional medicines will be planted as the garden grows and as guidance from the host Nations continues to shape its future.</p>
      <p>Today, the SFU Indigenous Plant Garden stands as a place for learning, reflection, and belonging. It is a space where people can come to sit with the medicines, learn from the land, reconnect with identity, teach outside of traditional classrooms, and experience the relationships that have always existed between people, plants, and place. The garden reflects resurgence, decolonization, cultural continuity, and the commitment to honour Indigenous knowledge as the heart of this work. It is both a beginning and a continuation, and a living story rooted in land, carried by community, and offered with gratitude to all who visit.</p>
    </div>
  </div>
</template>
