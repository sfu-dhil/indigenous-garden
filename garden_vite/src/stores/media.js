import { defineStore } from 'pinia'

const audioPlayer = new Audio();
audioPlayer.preload = 'none';

export const useMediaStore = defineStore('media', {
  state: () => ({
    currentAudio: null,
  }),
  getters: {},
  actions: {
    stopAllMedia() {
      this.stopAudio()
      document.querySelectorAll('audio').forEach( (audio) => {
        if (!audio.paused && !audio.ended) { audio.pause() }
      })
      document.querySelectorAll('video').forEach( (video) => {
        if (!video.paused && !video.ended) { video.pause() }
      })
    },
    stopAudio() {
      this.currentAudio = null
      audioPlayer.removeEventListener('ended', this.stopAudio)
      audioPlayer.removeEventListener('pause', this.stopAudio)
      if (audioPlayer.src) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
      }
    },
    toggleAudio(audio) {
      if (this.currentAudio === audio) {
        this.stopAudio()
      } else {
        this.currentAudio = audio
        audioPlayer.src = audio
        audioPlayer.play()
        audioPlayer.addEventListener('ended', this.stopAudio)
        audioPlayer.addEventListener('pause', this.stopAudio)
      }
    },
  },
  persist: false,
})
