
import { Offcanvas, Modal } from 'bootstrap'

export const toggleOffcanvas = (offcanvasEl, show) => {
  if (offcanvasEl) {
    const bsOffcanvas = Offcanvas.getOrCreateInstance(offcanvasEl)
    show ? bsOffcanvas.show() : bsOffcanvas.hide()
  }
}

export const toggleModal = (modalEl, show) => {
  if (modalEl) {
    const bsModal = Modal.getOrCreateInstance(modalEl)
    show ? bsModal.show() : bsModal.hide()
  }
}