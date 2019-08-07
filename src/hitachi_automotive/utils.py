import os
import json
import numpy as np
from skimage.draw import polygon


def rasterize_polygon(json_path, x_size, y_size):
    """Rasterize the polygon into a given size

    Args:
        json_path: Path to the JSON file
        x_size: size of the polygon image rasterized along the x-axis
        y_size: size of the polygon image rasterized along the y-axis

    Return:
        An numpy array of the size specified such as each cell value is the class id corresponding to these coordinates (default value is 0)"""

    nb_rows = y_size
    nb_cols = x_size

    # Open the JSON file
    with open(json_path, 'r') as f:
        dict_json = json.load(f)

    # Initialize a raster
    raster = np.zeros((nb_rows, nb_cols))

    # Define polygon
    poly = []
    for obj_id, obj_ctn in sorted(dict_json['objects'].items()):
        id_class = obj_ctn['classIndex']
        for dp_id, dp_ctn in sorted(obj_ctn['polygon'].items()):
            j_coord = np.round(dp_ctn['x'])
            i_coord = np.round(dp_ctn['y'])

            poly.append((i_coord, j_coord))

        rr, cc = polygon(poly[:, 0], poly[:, 1], (nb_rows, nb_cols))
        raster[rr, cc] = id_class

    return raster
