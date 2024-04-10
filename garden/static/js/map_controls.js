let {
    defaultDisplay,
} = document.currentScript.dataset;

// handle display toggling
const getDisplayType = () => localStorage.getItem('garden_display_type') || 'OVERHEAD';
const setDisplayType = displayType => {
    localStorage.setItem('garden_display_type', displayType);

    document.getElementById('overhead_map').style.display = displayType === 'OVERHEAD' ? 'block' : 'none';
    document.getElementById('pannellum_panorama').style.display = displayType === 'PANORAMA' ? 'block' : 'none';
};
setDisplayType(defaultDisplay || getDisplayType());
document.querySelectorAll('.select-map-control button').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        setDisplayType(btnEl.dataset.displayTypeToggle);
    });
});

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
const stopAllAudio = () => {
    document.querySelectorAll('audio').forEach( (audio) => {
        if (!audio.paused && !audio.ended) {
            audio.pause();
        }
    });
    if (nameAudioPlayer.src) {
        nameAudioPlayer.pause();
        nameAudioPlayer.currentTime = 0;
        updateNameAudioBtn();
    }
}
document.querySelectorAll('.name-audio-player').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        const wasPlaying = isNamedAudioPlayerPlaying();
        stopAllAudio();
        if (nameAudioBtnEl !== btnEl) {
            nameAudioBtnEl = btnEl;
            nameAudioPlayer.src = nameAudioBtnEl.dataset.src;
        } else if (wasPlaying) {
            return;
        }
        nameAudioPlayer.play();
    });
});

// handle off canvas
let offCanvas;
const hideFeatureOffcanvas = () => {
    if (!offCanvas) {
        return;
    }
    offCanvas.hide();
    offCanvas = null;
};
const toggleFeatureOffcanvas = (featureId, pointId, editPointType, hiddenCallback) => {
    const offCanvasEl = document.getElementById(`map-feature-${ featureId }`);
    const newOffCanvas = new bootstrap.Offcanvas(offCanvasEl);

    offCanvasEl.querySelectorAll('a.edit-point-btn').forEach ( linkEl => {
        if (pointId && editPointType) {
            linkEl.classList.remove('d-none');
            linkEl.href = `/admin/garden/${editPointType}/${ pointId }/change/`;
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
        stopAllAudio();
        offCanvas = null;
        offCanvasEl.removeEventListener('hide.bs.offcanvas', offcanvasHiddenEvent);
        if (hiddenCallback) {
            hiddenCallback();
        }
    });
    offCanvas.show();
}

const featuresHoverCallbacks = [];
const addFeaturesHoverCallback = (callback) => featuresHoverCallbacks.push(callback);
document.querySelectorAll('.feature-card-hover').forEach( (domEl) => {
    domEl.addEventListener('mouseover', () => {
        featuresHoverCallbacks.forEach( (callback) => {
            callback(domEl.dataset.featureId);
        })
    });
    domEl.addEventListener('mouseout', () => {
        featuresHoverCallbacks.forEach( (callback) => {
            callback();
        })
    });
});

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
document.querySelectorAll('.toggle-theme-btn').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        setTheme(btnEl.dataset.themeToggle);
    });
});

// enable tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// enable audio captions
document.querySelectorAll('.audio-with-captions').forEach( (domEl) => {
    const audioEl = domEl.querySelector('audio');
    const captionEl = domEl.querySelector('.figure-caption');
    const showCaptionsEl = domEl.querySelector('.show-captions-btn');
    const hideCaptionsEl = domEl.querySelector('.hide-captions-btn');

    showCaptionsEl.addEventListener('click', () => {
        domEl.classList.add('show-captions');
    });
    hideCaptionsEl.addEventListener('click', () => {
        domEl.classList.remove('show-captions');
    });

    for (const track of audioEl.textTracks) {
        if (track.kind == 'captions') {
            track.addEventListener('cuechange', () => {
                if (track.activeCues.length === 0) {
                    captionEl.innerHTML = '&nbsp;';
                } else {
                    captionEl.innerHTML = track.activeCues[0].text;
                }
            });
        }
    };
});