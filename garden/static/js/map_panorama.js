(() => {
    'use strict'

    const {
        imageUrl,
        isEdit,
        editPointId,
        isNew,
    } = document.currentScript.dataset;
    const pointsGroupedByFeatureId = Object.groupBy(
        JSON.parse(document.currentScript.dataset.points),
        ({ feature_id: featureId }) => featureId
    );

    const panoramaImage = new Image();
    panoramaImage.src = imageUrl;

    panoramaImage.onload = () => {
        const hotSpots = [];
        let editHotSpot, newHotSpot;

        // handle hover
        const setHoverFeatures = (hoverFeatureId) => {
            document.querySelectorAll('.hot-spot-wrapper').forEach( (domEl) => {
                domEl.dataset.featureId && domEl.dataset.featureId === hoverFeatureId ? domEl.classList.add('hover') : domEl.classList.remove('hover');
            });
        }
        addFeaturesHoverCallback( (featureId) => {
            setHoverFeatures(featureId);
        });

        for (const [featureId, points] of Object.entries(pointsGroupedByFeatureId)) {
            const number = points[0].number;

            const hotSpotTooltip = (hotSpotDiv) => {
                hotSpotDiv.innerHTML = `
                    <div class="hot-spot-wrapper hot-spot" data-feature-id="${featureId}">
                        <i class="fa-solid fa-location-pin" style="color: #7cb341"></i>
                        <span class="number-label">${number}</span>
                    </div>
                `;
                hotSpotDiv.addEventListener('mouseover', () => {
                    setHoverFeatures(featureId);
                });
                hotSpotDiv.addEventListener('mouseout', () => {
                    setHoverFeatures(null);
                });
            };
            points.forEach(point => {
                const {
                    id: pointId,
                    pitch,
                    yaw,
                } = point

                const hotSpot = {
                    pitch,
                    yaw,
                    type: 'info',
                    clickHandlerArgs: {
                        featureId,
                        pointId,
                    },
                    draggable: false,
                    cssClass: 'view-hotspot',
                    createTooltipFunc: hotSpotTooltip,
                };
                if (isEdit && editPointId == pointId) {
                    editHotSpot = hotSpot;
                }
                hotSpots.push(hotSpot);
            });
        };

        const pannellumViewer = pannellum.viewer('pannellum_panorama', {
            type: 'equirectangular',
            panorama: panoramaImage.src,
            // haov: 180,
            // vaov: 90,
            autoLoad: true,
            preview: panoramaImage.src,
            showControls: false,
            hotSpots: hotSpots,
            // hfov: 60,
            compass: true,
            // northOffset: 247.5
        });
        if (editHotSpot) {
            pannellumViewer.setPitch(editHotSpot.pitch, false);
            pannellumViewer.setYaw(editHotSpot.yaw, false);
        }
        document.getElementById('pannellum_zoom_in').addEventListener('click', function(e) {
            pannellumViewer.setHfov(pannellumViewer.getHfov() - 10);
        });
        document.getElementById('pannellum_zoom_out').addEventListener('click', function(e) {
            pannellumViewer.setHfov(pannellumViewer.getHfov() + 10);
        });

        // new point interaction
        if (isNew || isEdit) {
            const form_yaw_field = document.getElementById("id_yaw");
            const form_pitch_field = document.getElementById("id_pitch");

            const hotSpotEditTooltip = (hotSpotDiv) => {
                hotSpotDiv.innerHTML = `
                    <div class="hot-spot-wrapper hot-spot-edit">
                        <i class="fa-solid fa-location-pin"></i>
                    </div>
                `;
            };

            const handleHotSpotDrag = (event) => {
                if (["mouseup", "touchend", "pointerup"].includes(event.type)) {
                    const [
                        pitch,
                        yaw,
                    ] = pannellumViewer.mouseEventToCoords(event);

                    form_yaw_field.value = '' + yaw;
                    form_pitch_field.value = '' + pitch;
                }
            }

            if (isNew) {
                const addNewHotSpot = (coordinates) => {
                    const [
                        pitch,
                        yaw,
                    ] = coordinates;

                    newHotSpot = {
                        pitch,
                        yaw,
                        type: 'info',
                        draggable: true,
                        dragHandlerFunc: handleHotSpotDrag,
                        cssClass: 'edit-hotspot',
                        createTooltipFunc: hotSpotEditTooltip,
                    };

                    pannellumViewer.addHotSpot(newHotSpot);

                    // set initial form values
                    form_yaw_field.value = '' + yaw;
                    form_pitch_field.value = '' + pitch;
                };
                const addNewHotSpotClick = (event) => {
                    addNewHotSpot(pannellumViewer.mouseEventToCoords(event));
                    // remove click event
                    pannellumViewer.off('mouseup', addNewHotSpotClick);
                }

                // if coordinates already exist (failed save)
                if (form_pitch_field.value && !isNaN(parseFloat(form_pitch_field.value)) && form_yaw_field.value && !isNaN(parseFloat(form_yaw_field.value))) {
                    addNewHotSpot([parseFloat(form_pitch_field.value), parseFloat(form_yaw_field.value)])
                } else {
                    pannellumViewer.on('mouseup', addNewHotSpotClick);
                }
            } else if (editHotSpot) {
                editHotSpot.draggable = true;
                editHotSpot.dragHandlerFunc = handleHotSpotDrag;
                editHotSpot.cssClass = 'edit-hotspot';
                editHotSpot.createTooltipFunc = hotSpotEditTooltip;
            }
        // enable modals on read-only view
        } else {
            hotSpots.forEach((hotSpot) => {
                hotSpot.clickHandlerFunc = (hotSpot, args) => {
                    const {
                        featureId,
                        pointId,
                    } = args;
                    toggleFeatureOffcanvas(featureId, pointId, 'panoramapoint');
                }
            })
        }
    };
})()
