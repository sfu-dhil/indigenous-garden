// handle display toggling
document.querySelectorAll('.select-map-control button').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        setDisplayType(btnEl.dataset.displayTypeToggle);
    });
});

// handle multiple audio players
document.querySelectorAll('.click-audio-player').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        const wasPlaying = isNamedAudioPlayerPlaying();
        stopAllMedia();
        if (nameAudioBtnEl !== btnEl) {
            nameAudioBtnEl = btnEl;
            nameAudioPlayer.src = nameAudioBtnEl.dataset.src;
        } else if (wasPlaying) {
            return;
        }
        nameAudioPlayer.play();
    });
});

// handle feature card hover events
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
document.querySelectorAll('.toggle-theme-btn').forEach( (btnEl) => {
    btnEl.addEventListener('click', () => {
        setTheme(btnEl.dataset.themeToggle);
    });
});

// enable tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))