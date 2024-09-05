const {
    imageXyzPatternUrl,
    isEdit,
    editPointId,
    isNew,
} = document.currentScript.dataset;
const IMAGE_WIDTH = 2050;
const IMAGE_HEIGHT = 1510;
const featurePoints = JSON.parse(document.currentScript.dataset.featurePoints).sort((a, b) => {
    const max_a_y = Math.max(a.points.map((point) => point.y));
    const max_b_y = Math.max(b.points.map((point) => point.y));

    const min_a_x = Math.min(a.points.map((point) => point.x));
    const min_b_x = Math.min(b.points.map((point) => point.x));

    if (max_a_y > max_b_y) { return -1; }
    if (max_a_y < max_b_y) { return 1; }

    if (min_a_x < min_a_x) { return -1; }
    if (min_b_x > min_b_x) { return 1; }
    return 0;
})

// Map Layer
const imageExtent = [0, -IMAGE_HEIGHT, IMAGE_WIDTH, 0];
const viewExtent = [-IMAGE_WIDTH/2, -IMAGE_HEIGHT*3/2, IMAGE_WIDTH*1.5, IMAGE_HEIGHT*0.5];
const projection = new ol.proj.Projection({
    units: 'pixels',
    extent: imageExtent,
});
const imageTileLayer = new ol.layer.Tile({
    source: new ol.source.ImageTile({
        url: imageXyzPatternUrl,
        tileSize: [256, 256],
        maxResolution: 16,
        projection: projection,
    }),
});
const northRotation = (15.0 * Math.PI) / 180.0;
const view = new ol.View({
    projection: projection,
    center: ol.extent.getCenter(viewExtent),
    zoom: 2.5,
    minZoom: 1,
    maxZoom: 5,
    extent: viewExtent,
    rotation: northRotation,
});

// Feature Layers
const featureLayers = [];
let editFeature, newFeature;
for (const feature of featurePoints) {
    const {
        id: featureId,
        number,
        color: fillColor,
        feature_type: featureType,
        points,
    } = feature;

    const sourceVector = new ol.source.Vector({});
    points.forEach(point => {
        const {
            id: pointId,
            x,
            y,
        } = point
        const feature = new ol.Feature({
            geometry: new ol.geom.Point([x, y]),
            featureId,
            featureType,
            pointId,
        });
        if (isEdit && editPointId == pointId) {
            editFeature = feature;
        } else {
            sourceVector.addFeature(feature);
        }
    });
    const featureLayer = new ol.layer.Vector({
        source: sourceVector,
        featureId,
        featureType,
    });
    featureLayers.push(featureLayer);

    // style the layer
    const createThemedStyles = (theme) => {
        const strokeColor = theme === 'dark' ? 'white' : 'black'
        return [
            new ol.style.Style({
                text: new ol.style.Text({
                    text: '\uf041',
                    scale: 1.6,
                    textBaseline: 'bottom',
                    font: 'bold 1em "Font Awesome 6 Free"',
                    fill: new ol.style.Fill({ color: fillColor }),
                    stroke: new ol.style.Stroke({ color: strokeColor, width: 3 }),
                }),
            }),
            new ol.style.Style({
                text: new ol.style.Text({
                    text: `${number}`,
                    scale: 0.8,
                    textBaseline: 'bottom',
                    font: 'bold 1em "BC Sans"',
                    // offsetX: `${number}`.length - 1,
                    offsetY: -8,
                    fill: new ol.style.Fill({ color: strokeColor }),
                }),
            }),
        ]
    };
    const themedStyles = {
        light: createThemedStyles('light'),
        dark: createThemedStyles('dark'),
    }
    featureLayer.setStyle(themedStyles[getTheme()]);
    addToggleThemeCallback((theme) => {
        featureLayer.setStyle(themedStyles[theme]);
    });
};

const compassIcon = document.createElement('span');
compassIcon.innerHTML = `
    <span class="rotation-correction">
        ⇧
        <i class="fa-solid fa-n"></i>
    </span>
`;

const rotateControlButton = new ol.control.Rotate({
    autoHide: false,
    label: compassIcon,
    tipLabel: 'shift + drag mouse to rotate the map',
    resetNorth: () => {
        if (view.getRotation() % (2 * Math.PI) !== northRotation) {
            view.animate({
                rotation: northRotation,
                easing: ol.easing.easeOut,
            });
        }
    },
});

// map view
const map = new ol.Map({
    controls: ol.control.defaults.defaults().extend([
        rotateControlButton,
    ]),
    interactions: ol.interaction.defaults.defaults().extend([new ol.interaction.DragRotateAndZoom()]),
    layers: [
        imageTileLayer,
        ...featureLayers,
    ],
    view: view,
    target: 'map',
});
if (editFeature) {
    view.setCenter(editFeature.getGeometry().getCoordinates());
}

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

    const createThemedStyles = (theme) => {
        const strokeColor = theme === 'dark' ? 'white' : 'black'
        return [
            new ol.style.Style({
                text: new ol.style.Text({
                    text: '\uf041',
                    scale: 1.6,
                    textBaseline: 'bottom',
                    font: 'bold 16px "Font Awesome 6 Free"',
                    fill: new ol.style.Fill({ color: 'red' }),
                    stroke: new ol.style.Stroke({ color: strokeColor, width: 3 }),
                }),
            }),
        ]
    };
    const modifyThemedStyles = {
        light: createThemedStyles('light'),
        dark: createThemedStyles('dark'),
    }

    if (isNew) {
        const addNewFeature = (coordinates) => {
            newFeature = new ol.Feature({
                geometry: new ol.geom.Point(coordinates),
            });
            newFeature.setStyle(modifyThemedStyles[getTheme()]);
            addToggleThemeCallback((theme) => {
                newFeature.setStyle(modifyThemedStyles[theme]);
            })

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
        editFeature.setStyle(modifyThemedStyles[getTheme()]);
        addToggleThemeCallback((theme) => {
            editFeature.setStyle(modifyThemedStyles[theme]);
        })

        map.addLayer(new ol.layer.Vector({
            source: new ol.source.Vector({
                features: [editFeature]
            }),
        }));
        addDragInteraction(editFeature);
    }
// enable modals on read-only view
} else {

    const select = new ol.interaction.Select({
        style: null,
    });
    map.addInteraction(select);

    select.getFeatures().on('add', function(e) {
        const feature = e.element;
        const featureId = feature.get('featureId');
        const pointId = feature.get('pointId');
        toggleFeatureOffcanvas(featureId, pointId, () => {
            select.getFeatures().clear();
        });
    });

    select.getFeatures().on('remove', event => {
        hideFeatureOffcanvas();
    });

    // // Close the popup when the map is moved
    // map.on('movestart', () => {
    //     select.getFeatures().clear();
    // });
}

const hoverTextStroke = new ol.style.Stroke({ color: [13, 110, 253, 1], width: 3 });
let hoverLayer, oldLayerStroke;
const resetHoverLayer = () => {
    if (hoverLayer && oldLayerStroke) {
        const text = hoverLayer.getStyle()[0].getText();
        text.setStroke(oldLayerStroke);
        hoverLayer.changed()
    }
    hoverLayer = oldLayerStroke = null;
};
const setHoverLayer = (layer) => {
    if (hoverLayer === layer) {
        return;
    }
    resetHoverLayer();

    hoverLayer = layer;
    const text = hoverLayer.getStyle()[0].getText();
    oldLayerStroke = text.getStroke();
    text.setStroke(hoverTextStroke);

    hoverLayer.changed();
}
map.on("pointermove", function (evt) {
    const result = this.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
        return [feature, layer];
    });
    this.getTargetElement().style.cursor = (result) ? 'pointer' : '';

    const [_, layer] = result || [];
    layer ? setHoverLayer(layer) : resetHoverLayer();
});
addFeaturesHoverCallback( (featureId) => {
    if (!featureId) {
        resetHoverLayer();
        return;
    }
    const layers = map.getLayers().getArray().filter(
        (layer) => layer.get('featureId') == featureId
    );
    layers.length >= 1 ? setHoverLayer(layers[0]) : resetHoverLayer();
})