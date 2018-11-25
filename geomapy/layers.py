from .colors import *
import numpy as np

def fill_layer(layerId, sourceId, data, columnName, interpolate=False, cmap="plasma"):
    """
    Generates the JavaScript code for a map "fill" layer (i.e. polygons).
    Args:
      layerId (string): ID of the layer for MapBox
      sourceId (string): ID of the source (GeoJSON, etc.) for the data.
      data (DataFrame): DataFrame from geomapy.geojson2df() containing all the column info.
      columnName (string): The column to graph.
      interpolate (boolean): Whether or not the column is numeric.
      cmap (string): The name of the colormap to use.
    """
    if interpolate:
        colorscheme = interpolated_cm(
            [data[columnName].astype(np.float64).min(), data[columnName].astype(np.float64).max()],
            columnName,
            cmap_name=cmap)
    else:
        colorscheme = categorical_cm(
            set(data[columnName]),
            columnName
        )

    TEMPLATE = """
map.addLayer({{
    id:      "{layerId}",
    type:         "fill",
    source: "{sourceId}",
    layout:         {{}},
    paint: {{
        "fill-color": {colors},
        "fill-opacity": 0.75
    }}
}}, 'waterway-label');


map.on("click", "{layerId}", function(e) {{
    new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML("<b>{column}:</b> " + e.features[0].properties["{column}"])
        .addTo(map);
}});
"""

    return TEMPLATE.format(
        layerId=layerId,
        sourceId=sourceId,
        colors=colorscheme,
        column=columnName
    )
    
def circle_layer(layerId, sourceId, data, indexColumn, columnName, interpolate=False, cmap="viridis"):

    if cmap[0] == "#":
        colorscheme = "\"{}\"".format(cmap)
    else:
        if interpolate:
            colorscheme = interpolated_cm(
                [data[columnName].astype(np.float64).min(), data[columnName].astype(np.float64).max()],
                columnName,
                cmap_name=cmap)
        else:
            colorscheme = categorical_cm(
                set(data[columnName]),
                columnName,
                cmap_name=cmap
            )

    TEMPLATE = """
map.addLayer({{
    id:      "{layerId}",
    type:       "circle",
    source: "{sourceId}",
    layout:         {{}},
    paint: {{
        "circle-color": {colors},
        "circle-radius": {{
            "base":  1.5,
            "stops": [[6, 2], [12, 4], [18, 50], [22, 180]]
        }},
        "circle-opacity": 0.97
    }}
}}, 'waterway-label');

var {layerId}popup = new mapboxgl.Popup({{
    closeButton: false,
    closeOnClick: false
}});

map.on("mouseenter", "{layerId}", function(e) {{
    {layerId}popup
        .setLngLat(e.lngLat)
        .setHTML("<b>{index}:</b> " + e.features[0].properties["{index}"] + "<br>" +
                 "<b>{column}:</b> " + e.features[0].properties["{column}"])
        .addTo(map);
}});

map.on("mouseleave", "{layerId}", function(e) {{
    map.getCanvas().style.cursor = "";
    {layerId}popup.remove();
}});

map.setLayoutProperty("{layerId}", "visibility", "none");
"""

    return TEMPLATE.format(
        layerId=layerId,
        sourceId=sourceId,
        colors=colorscheme,
        index=indexColumn,
        column=columnName
    )