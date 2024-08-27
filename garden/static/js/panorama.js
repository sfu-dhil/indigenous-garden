(() => {
    'use strict'

    const player = videojs('panorama_video');
    player.vr({projection: '360'});

    const MIN_FOV = 30;
    const MAX_FOV = 110;
    const updateFov = (delta) => {
        if (player.vr().camera.fov + delta >= MIN_FOV && player.vr().camera.fov + delta <= MAX_FOV) {
            player.vr().camera.fov += delta;
            player.vr().camera.updateProjectionMatrix();
        }
    }
    document.getElementById('panorama_zoom_in').addEventListener('click', function(e) {
        updateFov(-10);
    });
    document.getElementById('panorama_zoom_out').addEventListener('click', function(e) {
        updateFov(10);
    });
    document.getElementById('panorama').addEventListener('wheel', function(e) {
        updateFov(e.deltaY * 0.01);
    });
})()
