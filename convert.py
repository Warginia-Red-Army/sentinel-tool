import os
from pathlib import Path

import rasterio
import numpy as np
from PIL import Image
import sys

def convert_raster(path):
    rgb_path = Path(path) / Path("response_rgb.tiff")
    output_path = Path(path.replace("raw", "output")) / "colored_rgb.png"
    print(f"Converting raster to tif {rgb_path}")
    with rasterio.open(str(rgb_path)) as src:
        blue = src.read(1)
        green = src.read(2)
        red = src.read(3)

    rgb = np.dstack([red,green,blue,]).astype(np.float32)
    rgb_norm = np.dstack([normalize(rgb[:,:,i]) for i in range(3)])
    os.makedirs(output_path.parent, exist_ok=True)
    Image.fromarray(rgb_norm).save(str(output_path))

def normalize(arr, low=2, high=98):
    lo, hi = np.percentile(arr, (low, high))
    arr = np.clip((arr - lo) / (hi - lo), 0, 1)
    return (arr*255).astype(np.uint8)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: path")
        sys.exit(1)

    path = sys.argv[1]
    convert_raster(path)