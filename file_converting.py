import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from data_converting import convert_true_color, convert_false_color, convert_ndvi, convert_swir_agriculture, \
    convert_urban_geology, convert_nbr, convert_ndmi

save_settings = {
    "ndvi": {
        "cmap": "RdYlGn",
        "percentile": (2, 98),
    },
    "ndmi": {
        "cmap": "BrBG",
        "percentile": (2, 98),
    },
    "nbr": {
        "cmap": "RdYlGn",
        "percentile": (2, 98),
    },
}

converters = {
    "N": ("ndvi", convert_ndvi),
    "T": ("true", convert_true_color),
    "F": ("false", convert_false_color),
    "M": ("ndmi", convert_ndmi),
    "B": ("nbr", convert_nbr),
    "S": ("swir", convert_swir_agriculture),
    "U": ("urban", convert_urban_geology),
}

def convert_image(folder, outs):
    results = []
    for key, (name, converter) in converters.items():
        if key in outs:
            print("Converting " + folder + " to " + name)
            results.append({
                "name": name,
                "data": converter(folder)
            })

    return results

def save_results(folder, result):
    folder = folder.replace("raw", "output")
    print("Saving results to " + folder)
    for r in result:
        path = Path(folder) / f"{r['name']}.png"

        settings = save_settings.get(r["name"], {}).copy()

        if "percentile" in settings:
            p_low, p_high = settings.pop("percentile")
            vmin, vmax = np.percentile(r["data"], (p_low, p_high))

            settings["vmin"] = vmin
            settings["vmax"] = vmax

        plt.imsave(
            str(path),
            r["data"],
            **settings
        )

def output_path_for(folder, name):
    out_folder = Path(str(folder).replace("raw", "output"))
    os.makedirs(out_folder, exist_ok=True)
    return out_folder / f"{name}.png"


def convert_images(folders, outs):
    if folders is not None:
        folders = [folders]
    if folders is None:
        base = Path("data/raw")
        folders = [scene_folder for scene_folder in base.iterdir() if scene_folder.is_dir()]

    for f in folders:
        results = convert_image(f, outs)
        save_results(f, results)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts raster files to png files")
    parser.add_argument("-i", "--input", required=False,
                        help="input scene folder (contains response_10m.tiff / response_20m.tiff)")
    parser.add_argument("-o", "--output", required=True,
                        help="which outputs to generate: T=true color, F=false color, N=ndvi, M=ndmi, B=nbr, S=swir/agri, U=urban/geology")

    args = parser.parse_args()
    convert_images(args.input, args.output)
