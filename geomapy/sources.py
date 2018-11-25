from .utils import geojson2df
from .layers import fill_layer, circle_layer
import numpy as np

def add_source(sourceId, file):
    TEMPLATE = """
map.addSource("{source}", {{
    type: "geojson",
    data: "/static/geojson/{file}"
}});
"""
    return TEMPLATE.format(
        source=sourceId,
        file=file
    )

def digest_dataset(file, columns, center=[-71.057083, 42.361145], overlays=[]):
    """
    """

    TEMPLATE = """
center = {center}
init_zoom = 11

map = createMap(center, init_zoom)

map.on("load", function() {{
    {source}

    {layers}
}})
"""

    dataset = geojson2df("./static/geojson/" + file)
    sourceId = file.replace(".geojson", "")
    source = add_source(sourceId, file)

    layers = []
    for columnName in columns:
        try:
            float(dataset[columnName][0])
            numeric = True
        except:
            numeric = False

        columnType = dataset[columnName].dtype

        try:
            layerId = columnName.replace(" ", "")

            layer = fill_layer(layerId,
                            sourceId,
                            dataset,
                            columnName,
                            interpolate=numeric,
                            cmap="plasma")
            layers.append(layer)
        except:
            print("Couldn't generate layer for {}".format(columnName))
    
    layers += overlays 

    js = TEMPLATE.format(
        center=center,
        source=source,
        layers="\n\n".join(layers)
    )

    return js, dataset


def digest_overlay(file, index, columns, cmap, center=[-71.057083, 42.361145]):
    """
    `columns` is list of columnNames
    """

    TEMPLATE = """
{source}

{layers}
"""

    dataset = geojson2df("./static/geojson/" + file)
    sourceId = file.replace(".geojson", "")
    source = add_source(sourceId, file)

    layers = []
    for columnName in columns:
        try:
            float(dataset[columnName][0])
            numeric = True
        except:
            numeric = False

        columnType = dataset[columnName].dtype

        # try:
        layerId = columnName.replace(" ", "")

        layer = circle_layer(layerId,
                            sourceId,
                            dataset,
                            index,
                            columnName,
                            interpolate=numeric,
                            cmap=cmap)
        layers.append(layer)
        # except:
        #     print("Couldn't generate layer for {}".format(columnName))
    
    js = TEMPLATE.format(
        source=source,
        layers="\n\n".join(layers)
    )

    return js