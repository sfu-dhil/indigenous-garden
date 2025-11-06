<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuRelationalInterconnectedTeachingsShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuRelationalInterconnectedTeachingsShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuRelationalInterconnectedTeachingsShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuRelationalInterconnectedTeachingsShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuRelationalInterconnectedTeachingsShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Relational and Interconnected Teachings</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <p>In Indigenous ways of knowing, nothing exists in isolation. Every being, including plants, animals, water, soil, and people, lives within a web of relationships. The Indigenous Plant Garden at SFU was designed with this teaching at its heart. Each of the twenty-four plants in the garden was intentionally chosen not only for its individual significance, but also for how it connects and thrives alongside others. This reflects an understanding that knowledge, like life itself, is relational.</p>
      <p>In many Indigenous worldviews, plants are recognized as kin and as living relatives who hold spirit, purpose, and agency. Their wellbeing depends on balance and reciprocity within their ecosystems. When one plant offers shade, another offers nitrogen; when one attracts pollinators, another benefits from their visit. Their relationships mirror the teachings that guide human communities: cooperation, respect, and care sustain life. Just as people need one another, so too do the plants.</p>
      <p>A well-known example of these relationships is the Three Sisters Garden, which combines corn, beans, and squash in an ancient agricultural system practiced by many Haudenosaunee and other Indigenous Nations. The corn provides a tall stalk for the beans to climb, the beans enrich the soil with nitrogen, and the squash spreads its broad leaves to retain moisture and deter weeds. Each plant contributes to the thriving of the others. This relationship is not merely practical but spiritual; it embodies the principle that strength comes through interdependence. The Three Sisters remind us that community is an ecosystem: diverse, balanced, and rooted in reciprocity.</p>
      <p>Though the SFU Indigenous Plant Garden does not include the Three Sisters, the same teachings are present. The plants here, exist in relation to each other and to the lands they come from. Their roots weave through the same soil, exchanging nutrients and messages through fungal networks. Some attract pollinators that benefit others; some thrive in the shade that neighbours provide. </p>
      <p>Douglas Fir provides the shade and protection that allow Salal, Sword Fern, and Oregon Grape to thrive in the understory. Together, they create layers of life, with each species supporting the others through shelter, nutrients, and shared habitat. The Huckleberry and Salal form thickets that feed birds, insects, and people alike, while their dense roots stabilize the soil and retain moisture for neighbouring plants.<sup><abbr title="Turner, N. J. (2005). The Earth's Blanket.">1</abbr></sup></p>
      <p>In the wetter areas, Red-Osier Dogwood, Pacific Ninebark, and Red Elderberry grow along the edges of water, binding the land together and filtering what flows through it. These plants act as translators between ecosystems, showing how life on the land and life in the water depend on one another.<sup><abbr title="Pojar &amp; MacKinnon (1994)">2</abbr></sup></p>
      <p>
        The Beaked Hazelnut carries another lesson of relationship. Recent research confirms what Indigenous peoples have long known: hazelnut groves were intentionally planted and tended by communities for thousands of years.<sup><abbr title="The Tyee, Dec 2024. &quot;Study Finds Indigenous People Cultivated Hazelnuts in BC 7,000 Years Ago.&quot; https://thetyee.ca/News/2024/12/04/Hazelnuts-Reveal-Secrets-Ancient-BC-City/"><a href="https://thetyee.ca/News/2024/12/04/Hazelnuts-Reveal-Secrets-Ancient-BC-City/">3</a></abbr></sup>
        They remind us that humans are part of the ecological web, not separate from it, and that caring for the land is a reciprocal act. The Vine Maple teaches balance at the forest edge, bridging sun and shade, growth and rest <sup><abbr title="Pojar & MacKinnon (1994)">4</abbr></sup>,
        while Baldhip Rose and Oceanspray offer materials and medicines that support both body and spirit.<sup><abbr title="Turner, N. J. (1998). Plant Technology of British Columbia First Peoples.">5</abbr></sup></p>
      <p></p>
      <p></p>
      <p></p>
      <p></p>
      <p></p>
      <p></p>
    </div>
  </div>
</template>


