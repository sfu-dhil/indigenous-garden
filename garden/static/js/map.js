let {
    mediaUrlPrefix,
    imageUrl,
    plants,
    canEdit,
    isEdit,
    editPointId,
    isNew,
} = document.currentScript.dataset;
plants = JSON.parse(plants);

let currentAudio, currentAudioEl;
const clearAudio = () => {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
    if (currentAudioEl) {
        // toggle icons
        currentAudioEl.classList.remove('bi-stop-circle');
        currentAudioEl.classList.add('bi-volume-up');
        currentAudioEl = null;
    }
};
const toggleAudio = (audioEl) => {
    const toggleCurrentlyPlaying = currentAudioEl == audioEl;
    clearAudio();
    if (toggleCurrentlyPlaying) {
        return;
    }
    currentAudioEl = audioEl;
    currentAudio = new Audio(audioEl.dataset.audioUrl);
    currentAudio.play();
    currentAudio.onended = () => {
        clearAudio();
    };
    // toggle icons
    audioEl.classList.remove('bi-volume-up');
    audioEl.classList.add('bi-stop-circle');
};

const mapImage = new Image();
mapImage.src = document.currentScript.dataset.imageUrl;
mapImage.onload = () => {
    // extent and projection
    const extent = [0, 0, mapImage.width, mapImage.height];
    const projection = new ol.proj.Projection({
        code: 'indigenous-garden',
        units: 'pixels',
        extent: extent,
    });

    const vectorLayers = [];

    let editFeature, newFeature;
    plants.forEach(plant => {
        const { number, color, points } = plant;
        const sourceVector = new ol.source.Vector({});
        // plant icon style (with number)
        const plantIconStyle = new ol.style.Style({
            image: new ol.style.FontSymbol({
                form: 'marker',
                text: number,
                font: 'sans-serif',
                fontSize: 0.7,
                fontStyle: 'bold',
                radius: 15,
                displacement: [0, 15],
                color: 'white',
                fill: new ol.style.Fill({
                    color: color,
                }),
                stroke: new ol.style.Stroke({
                    color: 'white',
                    width: 2,
                })
            }),
        });

        points.forEach(point => {
            const { id: pointId, x, y } = point

            const feature = new ol.Feature({
                geometry: new ol.geom.Point([x, y]),
                plant: plant,
                point: point,
            });
            if (isEdit && editPointId == pointId) {
                editFeature = feature;
            } else {
                feature.setStyle(plantIconStyle);
            }

            sourceVector.addFeature(feature);
        });

        vectorLayers.push(new ol.layer.Vector({
            source: sourceVector,
        }));
    })

    // map
    const map = new ol.Map({
        layers: [
            new ol.layer.Image({
                source: new ol.source.ImageStatic({
                    url: mapImage.src,
                    projection: projection,
                    imageExtent: extent,
                }),
            }),
            ...vectorLayers,
        ],
        target: 'map',
        view: new ol.View({
            projection: projection,
            center: ol.extent.getCenter(extent),
            zoom: 3,
            minZoom: 3,
            maxZoom: 5,
        }),
    });

    // new point interaction
    if (isNew || isEdit) {
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
        const modifyIconStyle = new ol.style.Style({
            image: new ol.style.FontSymbol({
                form: 'marker',
                font: 'sans-serif',
                fontSize: 0.7,
                fontStyle: 'bold',
                radius: 15,
                displacement: [0, 15],
                color: 'white',
                fill: new ol.style.Fill({
                    color: 'red',
                }),
                stroke: new ol.style.Stroke({
                    color: 'black',
                    width: 2,
                })
            }),
        });

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
            editFeature.setStyle(modifyIconStyle);
            addDragInteraction(editFeature);
        }
    // enable side menu on read-only view
    } else {
        const select = new ol.interaction.Select({
            style: null,
        });
        map.addInteraction(select);

        const plantInfoModalEl = document.getElementById('mapModal');
        const plantInfoModal = new bootstrap.Modal(plantInfoModalEl);

        const generateAudioTag = (audioUrl) => {
            if (audioUrl) {
                return `<i class="bi bi-volume-up" onClick="toggleAudio(this)" data-audio-url="${audioUrl}"></i>`;
            }
            return '';
        };

        select.getFeatures().on('add', function(e) {
            const feature = e.element;
            let {
                id: plantId,
                english_names, english_names_audio,
                english_content, english_content_audio,
                western_scientific_names, western_scientific_names_audio,
                halkomelem_names, halkomelem_names_audio,
                halkomelem_content, halkomelem_content_audio,
                squamish_names, squamish_names_audio,
                squamish_content, squamish_content_audio,
                images,
            } = feature.get('plant');
            let {
                id: pointId
            } = feature.get('point');

            // english fallback
            if (!halkomelem_names) {
                halkomelem_names = english_names;
                halkomelem_names_audio = english_names_audio;
            }
            if (!squamish_names) {
                squamish_names = english_names;
                squamish_names_audio = english_names_audio;
            }

            // title
            document.getElementById('mapModalTitle').innerHTML = `
                <span class="locale english">
                    ${english_names.join(' / ')}
                    ${generateAudioTag(english_names_audio)}
                    <p class="fw-lighter fst-italic fs-6">
                        ${western_scientific_names.join(' / ')}
                        ${generateAudioTag(western_scientific_names_audio)}
                    </p>
                </span>
                <span class="locale halkomelem">
                    ${halkomelem_names.join(' / ')}
                    ${generateAudioTag(halkomelem_names_audio)}
                </span>
                <span class="locale squamish">
                    ${squamish_names.join(' / ')}
                    ${generateAudioTag(squamish_names_audio)}
                </span>
            `;

            let carousel = '';
            if (images.length > 0) {
                const carouselIndicators = [];
                const carouselItems = [];
                images.forEach( (image, index) => {
                    let {
                        image: uploadedImage,
                        image_url: externalImage,
                        image_license,
                    } = image;

                    const active = index == 0 ? 'active' : '';
                    let imageTag = `
                        <svg class="bd-placeholder-img bd-placeholder-img-lg d-block w-100" width="800" height="400" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false">
                            <title>Placeholder</title>
                            <rect width="100%" height="100%" fill="#e5e5e5"></rect>
                        </svg>
                    `;
                    // internal image
                    if (uploadedImage) {
                        imageTag = `<img src="${uploadedImage}">`;
                    // external image
                    } else if (externalImage) {
                        imageTag = `<img src="${externalImage}">`;
                    }
                    carouselItems.push(`
                        <div class="carousel-item text-center ${active}">
                            ${imageTag}
                        </div>
                    `)
                    carouselIndicators.push(`
                        <button type="button" data-bs-target="#mapModalCarousel" data-bs-slide-to="${index}" class="${active}"></button>
                    `)
                });
                carousel = `
                    <div id="mapModalCarousel" class="carousel carousel-dark slide" data-bs-ride="false">
                        <div class="carousel-indicators">
                            ${carouselIndicators.join('\n')}
                        </div>
                        <div class="carousel-inner">
                            ${carouselItems.join('\n')}
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#mapModalCarousel" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#mapModalCarousel" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>
                `;
            }

            const editFooter = canEdit ? `
                <div class="modal-footer">
                    <a href="/admin/garden/plant/${plantId}/change/" class="btn btn-primary ms-auto"><i class="bi bi-pencil-square"></i> Edit plant</a>
                    <a href="/admin/garden/point/${pointId}/change/" class="btn btn-primary"><i class="bi bi-pencil-square"></i> Edit point</a>
                </div>
            ` : '';

            document.getElementById('mapModalBody').innerHTML = `
                ${carousel}
                <div>
                    <span class="locale english">
                        ${generateAudioTag(english_content_audio)}
                        ${english_content}
                    </span>
                    <span class="locale halkomelem">
                        ${generateAudioTag(halkomelem_content_audio)}
                        ${halkomelem_content}
                    </span>
                    <span class="locale squamish">
                        ${generateAudioTag(squamish_content_audio)}
                        ${squamish_content}
                    </span>
                </div>
                ${editFooter}
            `;

            if (images.length > 0) {
                const mapModalCarouselEl = document.querySelector('#mapModalCarousel')
                const mapModalCarousel = new bootstrap.Carousel(mapModalCarouselEl, {
                    wrap: true
                })
            }
            plantInfoModal.show();
        });

        select.getFeatures().on('remove', function(e) {
            clearAudio();
            plantInfoModal.hide();
            document.getElementById('mapModalBody').innerHTML = '';
        });

        // Close the popup when the map is moved
        map.on('movestart', () => {
            select.getFeatures().clear();
        });

        plantInfoModalEl.addEventListener('hidden.bs.modal', event => {
            select.getFeatures().clear();
        });
    }

    map.on("pointermove", function (evt) {
        const hit = this.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
            return true;
        });
        this.getTargetElement().style.cursor = (hit) ? 'pointer' : '';
    });
}
