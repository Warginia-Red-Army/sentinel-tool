import rasterio
import numpy as np

with rasterio.open("data/raw/2024-07-20_09_55/response_rgb.tiff") as src:
    print(src.count, src.dtypes, src.nodata)
    for i in range(1, src.count + 1):
        band = src.read(i)
        print(f"band {i}: min={band.min()}, max={band.max()}, unique values sample: {np.unique(band)[:10]}")