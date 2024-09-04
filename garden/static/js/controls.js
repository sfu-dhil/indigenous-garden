let {
    defaultDisplay,
    skipWelcomeModal,
} = document.currentScript.dataset;

// disable threejs warnings (and all js warnings in general)
const warn = console.warn;
console.warn = () => {};

// handle display toggling
const toggleDisplayCallbacks = [];
const addToggleDisplayCallback = (callback) => toggleDisplayCallbacks.push(callback);
const getDisplayType = () => localStorage.getItem('garden_display_type') || 'MAP';
const setDisplayType = displayType => {
    if (displayType != 'MAP' && displayType != 'PANORAMA') { displayType = 'MAP'; }
    localStorage.setItem('garden_display_type', displayType);
    document.getElementById('map').style.display = displayType === 'MAP' ? 'block' : 'none';
    document.getElementById('panorama').style.display = displayType === 'PANORAMA' ? 'block' : 'none';

    toggleDisplayCallbacks.forEach( (callback) => {
        callback(displayType);
    })
};
setDisplayType(defaultDisplay || getDisplayType());

// handle welcome modal on page load (only force show once per day)
const showWelcomeModal = () => {
    // don't show welcome modal when editing
    if (skipWelcomeModal) {
        return;
    }

    // only show the welcome modal if the cookie isn't set (uses cookie so that it can expire after 1 day)
    if (!document.cookie.split("; ").find((row) => row.startsWith("showWelcomeModal"))) {

        // set cookie to expire 1 day from now
        const exp = (new Date(Date.now() + 86400e3)).toUTCString();
        document.cookie = `showWelcomeModal=true; expires=${exp}; SameSite=None; Secure`;

        // show the modal
        const welcomeModal = new bootstrap.Modal(document.getElementById('welcome-model'));
        welcomeModal.show();
    }
}
showWelcomeModal();

// handle multiple audio players
let nameAudioBtnEl;
const nameAudioPlayer = new Audio();
nameAudioPlayer.preload = 'none';
const isNamedAudioPlayerPlaying = () => !!nameAudioPlayer.src && !nameAudioPlayer.paused && !nameAudioPlayer.ended;
const updateNameAudioBtn = () => {
    if (!nameAudioBtnEl) {
        return;
    }
    isNamedAudioPlayerPlaying() ? nameAudioBtnEl.classList.add('text-primary') : nameAudioBtnEl.classList.remove('text-primary');
}
nameAudioPlayer.addEventListener('ended', () => {
    nameAudioPlayer.currentTime = 0;
    updateNameAudioBtn();
});
nameAudioPlayer.addEventListener('pause', () => {
    updateNameAudioBtn();
});
nameAudioPlayer.addEventListener('play', () => {
    updateNameAudioBtn();
});
const stopAllMedia = () => {
    document.querySelectorAll('audio').forEach( (audio) => {
        if (!audio.paused && !audio.ended) {
            audio.pause();
        }
    });
    document.querySelectorAll('video').forEach( (video) => {
        if (!video.classList.contains('vjs-tech') && !video.paused && !video.ended) {
            video.pause();
        }
    });
    if (nameAudioPlayer.src) {
        nameAudioPlayer.pause();
        nameAudioPlayer.currentTime = 0;
        updateNameAudioBtn();
    }
}

// handle submenu off canvas
let subMenuOffCanvas;
const hideSubmenuOffcanvas = () => {
    if (!subMenuOffCanvas) {
        return;
    }
    subMenuOffCanvas.hide();
    subMenuOffCanvas = null;
};
const toggleSubmenuOffcanvas = (submenuId) => {
    const subMenuOffCanvasEl = document.getElementById(submenuId);
    const newSubMenuOffCanvas = new bootstrap.Offcanvas(subMenuOffCanvasEl);
    if (subMenuOffCanvas === newSubMenuOffCanvas) {
        return;
    }
    hideSubmenuOffcanvas();
    subMenuOffCanvas = newSubMenuOffCanvas;
    const subMenuOffCanvasHiddenEvent = subMenuOffCanvasEl.addEventListener('hide.bs.offcanvas', event => {
        subMenuOffCanvas = null;
        subMenuOffCanvasEl.removeEventListener('hide.bs.offcanvas', subMenuOffCanvasHiddenEvent);
    });
    subMenuOffCanvas.show();
}

// handle feature off canvas
let offCanvas;
const hideFeatureOffcanvas = () => {
    if (!offCanvas) {
        return;
    }
    offCanvas.hide();
    offCanvas = null;
};
const toggleFeatureOffcanvas = (featureId, pointId, hiddenCallback) => {
    const offCanvasEl = document.getElementById(`feature-${ featureId }`);
    const newOffCanvas = new bootstrap.Offcanvas(offCanvasEl);

    offCanvasEl.querySelectorAll('a.edit-point-btn').forEach ( linkEl => {
        if (pointId) {
            linkEl.classList.remove('d-none');
            linkEl.href = `/admin/garden/point/${ pointId }/change/`;
        } else {
            linkEl.classList.add('d-none');
        }
    });

    if (offCanvas === newOffCanvas) {
        return;
    }
    hideFeatureOffcanvas();
    offCanvas = newOffCanvas;
    const offcanvasHiddenEvent = offCanvasEl.addEventListener('hide.bs.offcanvas', event => {
        stopAllMedia();
        offCanvas = null;
        offCanvasEl.removeEventListener('hide.bs.offcanvas', offcanvasHiddenEvent);
        if (hiddenCallback) {
            hiddenCallback();
        }
    });
    offCanvas.show();
}

// handle feature card hover
const featuresHoverCallbacks = [];
const addFeaturesHoverCallback = (callback) => featuresHoverCallbacks.push(callback);

// color theme
const toggleThemeCallbacks = [];
const addToggleThemeCallback = (callback) => toggleThemeCallbacks.push(callback);
const getTheme = () => localStorage.getItem('garden_display_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
const setTheme = theme => {
    localStorage.setItem('garden_display_theme', theme);

    document.documentElement.setAttribute('data-bs-theme', theme);
    toggleThemeCallbacks.forEach( (callback) => {
        callback(theme);
    })
}
setTheme(getTheme());