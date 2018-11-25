import matplotlib as mpl
import matplotlib.pyplot as plt

def categorical_cm(categories, column, cmap_name="viridis"):
    """
    Returns the JavaScript code for creating
    a colormap based on categories.

    Args:
      categories (list of strings): The categories to generate colors for.
      column (string): The name of the column to graph.
      cmap_name (string): The name of the colormap to sample from.

    Returns:
      A JavaScript string containing the code for a categorical colorscheme.
    """
    cmap = plt.cm.get_cmap(cmap_name)
    ncats = len(categories)

    cats = []
    for ix, cat in enumerate(categories):
        rgb = cmap(ix / ncats)[:3]
        hexcode = mpl.colors.rgb2hex(rgb)
        cats.append("\"{}\", \"{}\"".format(cat, hexcode))
    
    TEMPLATE = """
[
    "match",
    ["get", "{column}"],
    {mappings},
    "#ccc"
]
    """
    return TEMPLATE.format(
        column=column,
        mappings=",\n".join(cats)
    )

def interpolated_cm(stops, column, cmap_name="rainbow"):
    """
    Returns the JavaScript code for creating
    a colormap based on certain stops.

    Args:
      stops (list of numeric): The values of the stops.
      column (string): The name of the column to graph.
      cmap_name (string): The name of the colormap to sample from.
    
    Returns:
      A string containing the JavaScript code for a numeric colorscheme.
    """
    cmap = plt.cm.get_cmap(cmap_name)
    nstops = len(stops)

    stop_strs = []
    for ix, stop in enumerate(stops):
        rgb = cmap(ix / nstops)[:3]
        hexcode = mpl.colors.rgb2hex(rgb)
        stop_strs.append("{}, \"{}\"".format(stop, hexcode))

    TEMPLATE = """
[
    "interpolate",
    ["linear"],
    ["to-number", ["get", "{column}"]],
    {stops}
]
    """
    return TEMPLATE.format(
        column=column,
        stops=",\n".join(stop_strs)
    )

if __name__ == "__main__":
    print(categorical_cm(["a", "b", "c"], "age"))
    print(interpolated_cm([0.0, 2000, 4000, 6000], "age"))