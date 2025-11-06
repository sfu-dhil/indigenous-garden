<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuContextualEthicalFramingShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuContextualEthicalFramingShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuContextualEthicalFramingShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuContextualEthicalFramingShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuContextualEthicalFramingShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Contextual and Ethical Framing</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <p>Completing the Indigenous Garden website is not simply a technical or educational task; it is an ethical one. Every word, image, and teaching shared through this space carries responsibility. Indigenous knowledge does not belong to an institution. It lives within relationships between people, lands, languages, and ancestors. To honour that, we must approach the garden not as a collection of information but as a living archive of relational knowledge and care.</p>
      <p>The Indigenous Garden is rooted in the lands and waters of Burnaby Mountain, within the traditional, ancestral, and unceded territories of the səlilwətaɬ (Tsleil-Waututh), kʷikʷəƛ̓əm (Kwikwetlem), Sḵwx̱wú7mesh Úxwumixw (Squamish) and xʷməθkʷəy̓əm (Musqueam) Nations. These lands are rich with teachings that long predate Simon Fraser University, and the garden itself grows from that living history. The plants here are more than species to study; they are relatives connected to place, story, and community. Their inclusion on this site is guided by respect for the peoples and lands who have cared for them since time immemorial.</p>
      <p>Indigenous knowledge systems are grounded in place. They are guided by languages that shape worldview, by ceremonies that renew balance, and by stories that teach how to live well with others. These ways of knowing hold deep ecological and spiritual understandings that have sustained communities and ecosystems for countless generations. When shared, they are offered as gifts, not as resources to extract. To privilege Indigenous knowledge, therefore, is to recognize it as complete, sovereign, and valid on its own terms; not in need of translation or comparison to Western frameworks.</p>
      <p>However, doing this work within an institutional context brings complexity. Universities are shaped by colonial histories that often prioritize Western scientific perspectives and methods of validation. Indigenous knowledge, which is relational, embodied, and often carried orally or ceremonially, can sit uneasily within systems built on ownership, authorship, and linear documentation. These tensions remind us that reconciliation is not about simply including Indigenous content; it is about transforming the structures that have long excluded or misrepresented it.</p>
      <p>Within this project, ethical framing means slowing down to ensure that consent, protocol, and relational accountability guide every step. Knowledge keepers must be engaged as equal partners, and their comfort, time, and community connections must be respected. Teachings cannot be separated from the people and Nations to whom they belong. This includes seeking permission before sharing, honouring the specific terms set by contributors, and ensuring that every piece of content is reviewed for cultural appropriateness and accuracy.</p>
      <p>Decolonization within digital and educational spaces means more than increasing visibility; it means shifting power. It asks institutions to listen rather than lead, to make space for Indigenous voices to shape the narrative, and to be willing to change processes when they cause harm or diminish cultural integrity. It also means recognizing that this work exists within living treaty relationships and responsibilities to the host Nations who have always cared for these territories.</p>
      <p>Cultural resurgence is another key part of this framing. To share Indigenous plant teachings publicly is not only to educate others but to revitalize knowledge within communities, particularly for younger generations who may be reconnecting with their identities and languages. Each teaching on this website contributes to that resurgence, inviting learners to see plants not as specimens but as relatives and living teachers who can guide us toward balance, respect, and renewal.</p>
      <p>Ethical use of this website also requires care from those who visit it. The teachings shared here are not meant to be copied or taken out of context. They are meant to be experienced as a whole, to be reflected upon, and to invite visitors into a respectful relationship with the plants and the knowledge keepers who have shared their wisdom. The purpose of this space is not to provide material to quote or extract, but to nurture understanding, curiosity, and connection. The knowledge on this site is relational, living, and sacred in its own right.</p>
      <p>Ethical stewardship also extends to how the garden and website evolve over time. This work must remain open to change, allowing for community feedback, updates, and additions as relationships grow. The measure of success is not how much information is collected but how well the process upholds respect, reciprocity, and responsibility.</p>
      <p>Ultimately, the Indigenous Garden and its digital companion stand as acts of relational accountability. They embody the possibility of doing institutional work in a good way through partnership, humility, and care. By centering Indigenous knowledge and ethical practice, we nurture a living bridge between land and learning, between digital space and sacred space, and between the responsibilities of today and the wisdom carried forward by generations to come.</p>
    </div>
  </div>
</template>
