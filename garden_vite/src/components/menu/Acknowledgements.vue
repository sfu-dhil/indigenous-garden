<script setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useDisplayStore } from '../../stores/display.js'
import { toggleOffcanvas } from '../../helpers/utils.js'

const displayStore = useDisplayStore()
const {
  menuAcknowledgementsShown,
} = storeToRefs(displayStore)

const offCanvasEl = useTemplateRef('menu-el')

watch(menuAcknowledgementsShown, (newValue, oldValue) => {
  if (newValue !== oldValue) { toggleOffcanvas(offCanvasEl.value, newValue) }
})
onMounted(() => {
  toggleOffcanvas(offCanvasEl.value, menuAcknowledgementsShown.value)
  offCanvasEl.value.addEventListener('hidden.bs.offcanvas', () => menuAcknowledgementsShown.value = false)
  offCanvasEl.value.addEventListener('shown.bs.offcanvas', () => menuAcknowledgementsShown.value = true)
})
</script>

<template>
  <div ref="menu-el" class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1">
    <div class="offcanvas-header">
      <h2 class="offcanvas-title h5">Acknowledgements</h2>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <p>The SFU Indigenous Plant Garden lives on the shared, unceded, and traditional territories of the səlilwətaɬ (Tsleil-Waututh), kʷikʷəƛ̓əm (Kwikwetlem), Sḵwx̱wú7mesh Úxwumixw (Squamish), and xʷməθkʷəy̓əm (Musqueam) Nations. With deep gratitude, we acknowledge the Peoples who have cared for these lands since time immemorial and whose languages, teachings, and relationships with the natural world continue to guide this work. We recognize Burnaby Mountain as a place of learning and connection where the plants, the soil, and the stories of these Nations remain alive and instructive.</p>
      <p>The Indigenous Plant Garden, together with its companion interactive website, was created in the spirit of respect and relationship. This project honours Indigenous knowledge systems and celebrates the ways that teachings are shared through land, story, and community. The website extends the living garden into a digital space of reflection and reciprocity, where visitors are invited to learn from the plants and the words of the knowledge keepers who have so generously shared their wisdom. Rooted in place, guided by protocol, and offered with care, this is a space for gratitude, learning, and renewal.</p>
      <p>The creation of the Indigenous Plant Garden and this interactive website has been a collective effort grounded in relationship, reciprocity, and shared vision. Many people and partners have walked alongside this work, contributing their time, knowledge, creativity, and care. Each person acknowledged here has played an important role in shaping the garden’s spirit; whether through sharing teachings, supporting the planting and maintenance of the space, guiding its educational purpose, or helping bring the stories of the plants to life in digital form. We offer our heartfelt gratitude to all who have contributed to the growth of this living place of learning.</p>

      <hr class="my-4" />
      <h4>Knowledge Keepers and Cultural Advisors</h4>
      <ul class="list-group mb-3">
        <li class="list-group-item list-group-item-action">Fern Gabriel (Kwikwetlem Nation)</li>
        <li class="list-group-item list-group-item-action">Paula James (Kwantlen Nation) </li>
        <li class="list-group-item list-group-item-action">Victor Guerin (xʷməθkʷəy̓əm)</li>
        <li class="list-group-item list-group-item-action">Aaron Williams (Sḵwx̱wú7mesh Úxwumixw)</li>
        <li class="list-group-item list-group-item-action">Senaqwila Wyss (Sḵwx̱wú7mesh Úxwumixw)</li>
        <li class="list-group-item list-group-item-action">Cease Wyss (Sḵwx̱wú7mesh Úxwumixw)</li>
        <li class="list-group-item list-group-item-action">Aaron "Splash" Moody (Sḵwx̱wú7mesh Úxwumixw)</li>
        <li class="list-group-item list-group-item-action">Leslhá7lhamaat Elizabeth Ross (Sḵwx̱wú7mesh Úxwumixw)</li>
        <li class="list-group-item list-group-item-action">Chelsey Armstrong (Assistant Professor, Indigenous Studies)</li>
        <li class="list-group-item list-group-item-action">Leateeqwhia Daniels & Tracy Williams (Curriculum Development, Squamish Nation)</li>
        <li class="list-group-item list-group-item-action">Elroy Baker (Sḵwx̱wú7mesh Úxwumixw)</li>
      </ul>
      <p>Their teachings remind us that plants are kin and that knowledge lives in relationship. Each teaching shared here remains held by the individuals and Nations who offered them.</p>

      <hr class="my-4" />
      <h4>Project Leads and Collaborators</h4>
      <ul class="list-group mb-3">
        <li class="list-group-item list-group-item-action">Jennie Blenkinship &dash; Project Founder and Vision Holder</li>
        <li class="list-group-item list-group-item-action">Sara Davidson &dash; Cultural and Educational Advisor</li>
        <li class="list-group-item list-group-item-action">Ron Johnston &dash; Office for Aboriginal Peoples </li>
        <li class="list-group-item list-group-item-action">Estelle D'Souza &dash; Communications and Coordination Support </li>
        <li class="list-group-item list-group-item-action">Lindsay Heller &dash; Consultant and Project advisor and Videographer</li>
        <li class="list-group-item list-group-item-action">Sulan Ramdeen &dash; Research Assistant</li>
        <li class="list-group-item list-group-item-action">Reshme Kumar &dash; Research Assistant</li>
        <li class="list-group-item list-group-item-action">Calder Cheverie &dash; Videographer</li>
        <li class="list-group-item list-group-item-action">Pablo Vimos &dash; Garden Educator</li>
        <li class="list-group-item list-group-item-action">Kathleen Aldridge &dash; Coordinator, Special Project</li>
        <li class="list-group-item list-group-item-action">Jennifer Reddington &dash; Director, Innovation and Infrastructure</li>
      </ul>
      <p>These individuals helped bring the garden and website to life through vision, collaboration, and commitment to decolonizing practice and community relationships.</p>

      <hr class="my-4" />
      <h4>Host Nations</h4>
      <p>With gratitude to the səlilwətaɬ (Tsleil-Waututh), kʷikʷəƛ̓əm (Kwikwetlem), Sḵwx̱wú7mesh Úxwumixw (Squamish), and xʷməθkʷəy̓əm (Musqueam) Nations, the original caretakers of Burnaby Mountain. Their enduring relationships with these lands guide the spirit and responsibility of this project.</p>

      <hr class="my-4" />
      <h4>Community Partners, Sponsors, and Supporters</h4>
      <ul class="list-group mb-3">
        <li class="list-group-item list-group-item-action">Dan Laitsch (Dean, Faculty of Education)</li>
        <li class="list-group-item list-group-item-action">Larry Waddell (Chief Facilities Officer, Facility Services)</li>
        <li class="list-group-item list-group-item-action">Wade Parkhouse (Associate Vice-President, Academic)</li>
        <li class="list-group-item list-group-item-action">Sara Davidson, Isabelle Cote, Robyn Ilten-Gee (IERC Co-Chairs)</li>
        <li class="list-group-item list-group-item-action">Bryan Myles and Natahnee Winder (Bill Reid Centre)</li>
        <li class="list-group-item list-group-item-action">Sobhana Jaya-Madhavan, Ron Johnston, and ARC Co-Facilitators (ASI/ARC)</li>
        <li class="list-group-item list-group-item-action">Matthew Grant (Centre for Educational Innovation)</li>
        <li class="list-group-item list-group-item-action">UA Local 170</li>
        <li class="list-group-item list-group-item-action">Krystal Ness and Megan Murphy (Facilities &dash; Buildings and Grounds)</li>
        <li class="list-group-item list-group-item-action">Rebecca Dowson and Andrew Gardener (Digital Scholarship Librarian and Developer, DHIL Team)</li>
        <li class="list-group-item list-group-item-action">Greg Thrift (Manager, Exterior Services)</li>
        <li class="list-group-item list-group-item-action">Greg Hamm (Corporate Services and Communications, Second City PS)</li>
        <li class="list-group-item list-group-item-action">Document Solutions (SFU)</li>
        <li class="list-group-item list-group-item-action">Robert Badringa (Assistant Professor of Professional Practice, Indigenous Studies)</li>
        <li class="list-group-item list-group-item-action">Kim Peterson (Designer, Communications and Marketing)</li>
        <li class="list-group-item list-group-item-action">Melissa Hudson (Manager, Communications and Marketing)</li>
        <li class="list-group-item list-group-item-action">Suzanne Smythe (Associate Professor, Academic Coordinator, Faculty Teaching Fellow)</li>
        <li class="list-group-item list-group-item-action">Cher Hill (Assistant Professor) </li>
      </ul>
      <p>Each of these contributors provided essential support through funding, facilities coordination, digital development, or hands-on participation to ensure the success and sustainability of the garden and its digital home.</p>
    </div>
  </div>
</template>
