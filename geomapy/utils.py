import json
import pandas as pd

def geojson2df(file):
    geojson = json.load(open(file))
    all_features = []
    for feature in geojson["features"]:
        properties = dict(feature["properties"])
        properties["geometry"] = feature["geometry"]
        all_features.append(properties)
    return pd.DataFrame.from_dict(all_features)

if __name__ == "__main__":
    print(geojson2df("boston_neighborhoods.geojson"))
