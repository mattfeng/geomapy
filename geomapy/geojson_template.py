import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

GEOJSON_TEMPLATE = """
{{
  "type": "FeatureCollection",
  "features": [
    {features}
  ]
}}
"""

POINT_TEMPLATE = """
{{
  "type": "Feature",
  "geometry": {{
    "type": "Point",
    "coordinates": {coord}
  }},
  "properties": {{
    {props}
  }}
}}
"""

POINT_GEOMETRY_TEMPLATE = """
{{
  "type": "Point",
  "coordinates": [{lng}, {lat}]
}}
"""

FEATURE_TEMPLATE = """
{{
  "type": "Feature",
  "geometry": {geometry},
  "properties": {{
      {props}
  }}
}}
"""

# CSV -> GeoJSON -> Mapbox Layers
def flip_lat_lng(coord):
    a, b = coord.replace(" ", "").strip("()").split(",")
    return "[{}, {}]".format(b, a)


def point_set(df, coord, properties, transform=lambda x: x):
    point_features = []
    for _, row in df.iterrows():
        feature = point_feature(transform(row[coord]), {p:row[p] for p in properties})
        point_features.append(feature)

    return GEOJSON_TEMPLATE.format(
        features=",".join(point_features)
    )


def point_feature(coord, properties):
    props_string = ",".join(
        '"{}": {}'.format(key, repr(val))
        for key, val in properties.items()
    )

    return POINT_TEMPLATE.format(
        coord=coord,
        props=props_string)


def feature(row, props):
    props_string = ",".join(
        '"{}": {}'.format(prop, repr(row[prop]).replace("'", "\""))
        for prop in props
    )

    return FEATURE_TEMPLATE.format(
        geometry=str(row["geometry"]).replace("'", "\""),
        props=props_string)


def feature_set(df, props):
    features = []
    for _, row in df.iterrows():
        features.append(
            feature(row, props)
        )
    return GEOJSON_TEMPLATE.format(
        features=",".join(features)
    )


if __name__ == "__main__":
    # feature = point_feature((12.3, 45.6), {"name":"hello"})
    # print(feature)
    # df = pd.read_csv("../test_data/liquor-licenses.csv")
    # df = df.iloc[:10, :]
    # print(point_set(df, "Location", ["CAPACITY"], transform=flip_lat_lng))
    pass