let {
    mediaUrlPrefix,
    imageUrl,
    mapFeatures,
    forceDisplay,
    canEdit,
    isEdit,
    editPointId,
    isNew,
} = document.currentScript.dataset;
mapFeatures = JSON.parse(mapFeatures);

// handle display toggling
let currentDisplayType = localStorage.getItem('garden_display_type') || 'OVERHEAD';
const showDisplay = () => {
    if (currentDisplayType === 'OVERHEAD') {
        document.getElementById('overhead_map').style.display = "block";
        document.getElementById('pannellum_panorama').style.display = "none";
    } else {
        document.getElementById('overhead_map').style.display = "none";
        document.getElementById('pannellum_panorama').style.display = "block";
    }
}
const setDisplayType = (displayType) => {
    currentDisplayType = displayType;
    localStorage.setItem('garden_display_type', displayType);
    showDisplay()
}
setDisplayType(forceDisplay || currentDisplayType);

if (forceDisplay) {
    document.getElementById('toggle_display_to_overhead').classList.add("d-none");
    document.getElementById('toggle_display_to_panorama').classList.add("d-none");
} else {
    document.getElementById('toggle_display_to_overhead').addEventListener('click', function(e) {
        setDisplayType('OVERHEAD');
    });
    document.getElementById('toggle_display_to_panorama').addEventListener('click', function(e) {
        setDisplayType('PANORAMA');
    });
}


// load images
const overheadImage = new Image();
overheadImage.src = document.currentScript.dataset.overheadImageUrl;
const overheadImagePromise = new Promise((resolve, reject) => {
    overheadImage.onload = () => { resolve(); };
    overheadImage.onerror = () => { reject(); };
});

const panoramaImage = new Image();
panoramaImage.src = document.currentScript.dataset.panoramaImageUrl;
const panoramaImagePromise = new Promise((resolve, reject) => {
    panoramaImage.onload = () => { resolve(); };
    panoramaImage.onerror = () => { reject(); };
});

Promise.all([overheadImagePromise, panoramaImagePromise]).then(() => {
    // Overhead Layer
    const extent = [0, 0, overheadImage.width, overheadImage.height];
    const projection = new ol.proj.Projection({
        code: 'static-image-garden',
        units: 'pixels',
        extent: extent,
    });
    const imageLayer = new ol.layer.Image({
        source: new ol.source.ImageStatic({
            url: overheadImage.src,
            projection: projection,
            imageExtent: extent,
        }),
    });
    const view = new ol.View({
        projection: projection,
        center: ol.extent.getCenter(extent),
        zoom: 3,
        minZoom: 1,
        maxZoom: 5,
        extent: extent,
    });

    // Feature Layers
    const featureLayers = [];
    let editFeature, newFeature;
    mapFeatures.forEach(mapFeature => {
        const { number, color, overhead_points } = mapFeature;
        const sourceVector = new ol.source.Vector({});

        // feature icon style (with number)
        const featureIconStyles = [
            new ol.style.Style({
                text: new ol.style.Text({
                    text: '\uf041',
                    scale: 1.6,
                    textBaseline: 'bottom',
                    font: 'bold 16px "Font Awesome 6 Free"',
                    fill: new ol.style.Fill({ color: color }),
                    stroke: new ol.style.Stroke({ color: 'white', width: 3 }),
                }),
                zIndex: 1,
            }),
            new ol.style.Style({
                text: new ol.style.Text({
                    text: `${number}`,
                    scale: 0.8,
                    textBaseline: 'bottom',
                    font: 'bold 16px "BC Sans"',
                    // offsetX: `${number}`.length - 1,
                    offsetY: -8,
                    fill: new ol.style.Fill({ color: 'white' }),
                }),
                zIndex: 2,
            }),
        ];

        overhead_points.forEach(point => {
            const {
                id: pointId,
                x,
                y,
            } = point
            const feature = new ol.Feature({
                geometry: new ol.geom.Point([x, y]),
                mapFeature: mapFeature,
                point: point,
            });
            if (isEdit && editPointId == pointId && forceDisplay === 'OVERHEAD') {
                editFeature = feature;
            } else {
                feature.setStyle(featureIconStyles);
            }
            sourceVector.addFeature(feature);
        });

        featureLayers.push(new ol.layer.Vector({
            source: sourceVector,
        }));
    });

    // overhead map
    const map = new ol.Map({
        layers: [
            imageLayer,
            ...featureLayers,
        ],
        view: view,
        target: 'overhead_map',
    });

    const hotSpots = [];
    let editHotSpot, newHotSpot;
    mapFeatures.forEach(mapFeature => {
        const { number, color, panorama_points } = mapFeature;

        const hotSpotTooltip = (hotSpotDiv) => {
            hotSpotDiv.innerHTML = `
                <div class="hot-spot-wrapper hot-spot">
                    <i class="fa-solid fa-location-pin" style="color: ${color}"></i>
                    <span class="number-label">${number}</span>
                </div>
            `;
        };

        panorama_points.forEach(point => {
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
                    mapFeature,
                    pointId,
                },
                draggable: false,
                cssClass: 'view-hotspot',
                createTooltipFunc: hotSpotTooltip,
            };
            if (isEdit && editPointId == pointId && forceDisplay === 'PANORAMA') {
                editHotSpot = hotSpot;
            }
            hotSpots.push(hotSpot);
        });
    });
    const pannellumViewer = pannellum.viewer('pannellum_panorama', {
        type: 'equirectangular',
        panorama: panoramaImage.src,
        haov: 180,
        vaov: 90,
        autoLoad: currentDisplayType === 'PANORAMA',
        preview: panoramaImage.src,
        // "showFullscreenCtrl": false,
        showControls: false,
        hotSpots: hotSpots,
        hfov: 60,
    });
    document.getElementById('pannellum_zoom_in').addEventListener('click', function(e) {
        pannellumViewer.setHfov(pannellumViewer.getHfov() - 10);
    });
    document.getElementById('pannellum_zoom_out').addEventListener('click', function(e) {
        pannellumViewer.setHfov(pannellumViewer.getHfov() + 10);
    });

    // new point interaction
    if (isNew || isEdit) {
        if (forceDisplay === 'OVERHEAD') {
            const form_x_field = document.getElementById("id_x");
            const form_y_field = document.getElementById("id_y");

            const addDragInteraction = (feature) => {
                const dragInteraction = new ol.interaction.Modify({
                    features: new ol.Collection([feature]),
                    style: null,
                });
                map.addInteraction(dragInteraction)

                feature.on('change', function() {
                    form_x_field.value = '' + this.getGeometry().getCoordinates()[0];
                    form_y_field.value = '' + this.getGeometry().getCoordinates()[1];
                }, feature);
            }

            const modifyIconStyles = [
                new ol.style.Style({
                    text: new ol.style.Text({
                        text: '\uf041',
                        scale: 1.6,
                        textBaseline: 'bottom',
                        font: 'bold 16px "Font Awesome 6 Free"',
                        fill: new ol.style.Fill({ color: 'red' }),
                        stroke: new ol.style.Stroke({ color: 'black', width: 3 }),
                    }),
                    zIndex: 1,
                }),
            ];

            if (isNew) {
                const addNewFeature = (coordinates) => {
                    newFeature = new ol.Feature({
                        geometry: new ol.geom.Point(coordinates),
                    });
                    newFeature.setStyle(modifyIconStyle);

                    map.addLayer(new ol.layer.Vector({
                        source: new ol.source.Vector({
                            features: [newFeature]
                        }),
                    }));
                    addDragInteraction(newFeature);

                    // set initial form values
                    form_x_field.value = '' + coordinates[0];
                    form_y_field.value = '' + coordinates[1];
                };
                const addNewFeatureClick = (evt) => {
                    addNewFeature(evt.coordinate);

                    // remove click event
                    map.un('click', addNewFeatureClick);
                }

                // if coordinates already exist (failed save)
                if (form_x_field.value && !isNaN(parseFloat(form_x_field.value)) && form_y_field.value && !isNaN(parseFloat(form_y_field.value))) {
                    addNewFeature([parseFloat(form_x_field.value), parseFloat(form_y_field.value)])
                } else {
                    map.on('click', addNewFeatureClick);
                }
            } else if (editFeature) {
                editFeature.setStyle(modifyIconStyles);
                addDragInteraction(editFeature);
            }
        } else if (forceDisplay === 'PANORAMA') {
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
                console.log('event', event)
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
        }
    // enable modals on read-only view
    } else {
        const select = new ol.interaction.Select({
            style: null,
        });
        map.addInteraction(select);

        const featureInfoModalEl = document.getElementById('modal');
        const featureInfoModal = new bootstrap.Modal(featureInfoModalEl);

        const setupModal = (mapFeature, pointId) => {
            const {
                id: featureId,
                feature_type,
                audio,
                english_names,
                western_scientific_names,
                halkomelem_names,
                squamish_names,
                content,
                images,
            } = mapFeature;

            const formatNames = (items, color) => {
                const colorIcon = color ? `<i class="bi bi-circle-fill fs-6" style="color: ${color}"></i> ` : '';
                return items.map(item => {
                    return colorIcon + (item.descriptor ? `${item.name} <small class="text-muted">(${item.descriptor})</small>` : item.name)
                }).join(' <br /> ');
            }

            // title
            document.getElementById('modalTitle').innerHTML = `
                <div class="row">
                    <div class="col-md">
                        ${formatNames(english_names)}
                        <p class="fw-lighter fst-italic fs-6">
                            ${formatNames(western_scientific_names)}
                        </p>
                    </div>
                    <div class="col-md">
                        ${formatNames(halkomelem_names, '#64c4cf')}
                    </div>
                    <div class="col-md">
                        ${formatNames(squamish_names, '#7cb341')}
                    </div>
                </div>
            `;

            let carousel = '';
            if (images.length > 0) {
                const carouselIndicators = [];
                const carouselItems = [];
                images.forEach( (image, index) => {
                    const {
                        image: uploadedImage,
                        image_url: externalImage,
                        image_license,
                    } = image;
                    const imageUrl = uploadedImage || externalImage || null;

                    const active = index == 0 ? 'active' : '';
                    let imageTag = `
                        <svg class="bd-placeholder-img bd-placeholder-img-lg d-block w-100" width="800" height="400" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false">
                            <title>Placeholder</title>
                            <rect width="100%" height="100%" fill="#e5e5e5"></rect>
                        </svg>
                    `;
                    if (imageUrl) {
                        imageTag = `<img src="${imageUrl}" class="img-fluid">`;
                    }
                    carouselItems.push(`
                        <div class="carousel-item text-center ${active}">
                            ${imageTag}
                        </div>
                    `)
                    carouselIndicators.push(`
                        <button type="button" data-bs-target="#modalCarousel" data-bs-slide-to="${index}" class="${active}"></button>
                    `)
                });
                carousel = `
                    <div id="modalCarousel" class="carousel carousel-dark slide" data-bs-ride="false">
                        <div class="carousel-indicators">
                            ${carouselIndicators.join('\n')}
                        </div>
                        <div class="carousel-inner">
                            ${carouselItems.join('\n')}
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#modalCarousel" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#modalCarousel" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>
                `;
            }

            const audioTag = audio ? `<br /><audio controls preload="metadata" src="${audio}" class="w-100"></audio><br />` : '';
            document.getElementById('modalBody').innerHTML = `
                ${carousel}
                <div>
                    ${audioTag}
                    ${content}
                </div>
            `;

            if (canEdit) {
                const pointSubpath = currentDisplayType === 'OVERHEAD' ? `overheadpoint` : `panoramapoint`;

                document.getElementById('modalFooter').classList.remove("d-none");
                document.getElementById('modalFooter').innerHTML = `
                    <a href="/admin/garden/feature/${featureId}/change/" class="btn btn-primary ms-auto"><i class="bi bi-pencil-square"></i> Edit feature</a>
                    <a href="/admin/garden/${pointSubpath}/${pointId}/change/" class="btn btn-primary"><i class="bi bi-pencil-square"></i> Edit point</a>
                `;
            } else {
                document.getElementById('modalFooter').classList.add("d-none");
            }

            if (images.length > 0) {
                const modalCarouselEl = document.querySelector('#modalCarousel')
                const modalCarousel = new bootstrap.Carousel(modalCarouselEl, {
                    wrap: true
                })
            }
            featureInfoModal.show();
        }

        select.getFeatures().on('add', function(e) {
            const feature = e.element;
            const mapFeature = feature.get('mapFeature');
            const {
                id: pointId,
            } = feature.get('point');
            setupModal(mapFeature, pointId);
        });

        select.getFeatures().on('remove', function(e) {
            featureInfoModal.hide();
            document.getElementById('modalBody').innerHTML = '';
        });

        // Close the popup when the map is moved
        map.on('movestart', () => {
            select.getFeatures().clear();
        });

        featureInfoModalEl.addEventListener('hidden.bs.modal', event => {
            select.getFeatures().clear();
        });

        hotSpots.forEach((hotSpot) => {
            hotSpot.clickHandlerFunc = (hotSpot, args) => {
                const {
                    mapFeature,
                    pointId,
                } = args;
                setupModal(mapFeature, pointId);
            }
        })
    }

    map.on("pointermove", function (evt) {
        const hit = this.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
            return true;
        });
        this.getTargetElement().style.cursor = (hit) ? 'pointer' : '';
    });
});
