import os
from pathlib import Path

import rasterio
from rasterio.enums import Resampling
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse

# --- pomocnicze ---

def normalize(arr, low=2, high=98):
    lo, hi = np.percentile(arr, (low, high))
    arr = np.clip((arr - lo) / (hi - lo), 0, 1)
    return (arr * 255).astype(np.uint8)


def read_resampled_band(path_20m, band_idx, target_shape):
    with rasterio.open(str(path_20m)) as src:
        data = src.read(
            band_idx,
            out_shape=(target_shape[0], target_shape[1]),
            resampling=Resampling.bilinear
        )
    return data.astype(np.float32)


def output_path_for(folder, name):
    out_folder = Path(str(folder).replace("raw", "output"))
    os.makedirs(out_folder, exist_ok=True)
    return out_folder / f"{name}.png"


# --- kompozycje z jednego pliku (10m) ---

def convert_raster(folder, bands=(3, 2, 1), name="unknown"):
    rgb_path = Path(folder) / "response_10m.tiff"
    with rasterio.open(str(rgb_path)) as src:
        red = src.read(bands[0])
        green = src.read(bands[1])
        blue = src.read(bands[2])

    rgb = np.dstack([red, green, blue]).astype(np.float32)
    rgb_norm = np.dstack([normalize(rgb[:, :, i]) for i in range(3)])

    out = output_path_for(folder, name)
    Image.fromarray(rgb_norm).save(str(out))
    print(f"Saved {out}")


def convert_true_color(folder):
    convert_raster(folder, bands=(3, 2, 1), name="true_color")


def convert_false_color(folder):
    convert_raster(folder, bands=(4, 3, 2), name="false_color")


# --- wskaźniki z jednego pliku (10m): NDVI ---

def compute_index_single(folder, path_tiff, band_a_idx, band_b_idx, name, cmap="RdYlGn"):
    with rasterio.open(str(path_tiff)) as src:
        band_a = src.read(band_a_idx).astype(np.float32)
        band_b = src.read(band_b_idx).astype(np.float32)

    denom = band_a + band_b
    denom[denom == 0] = 1e-6
    index = (band_a - band_b) / denom

    print(f"{name}: min={index.min():.3f}, max={index.max():.3f}, mean={index.mean():.3f}")
    vmin, vmax = np.percentile(index, (2, 98))

    out = output_path_for(folder, name)
    plt.imsave(str(out), index, cmap=cmap, vmin=vmin, vmax=vmax)
    print(f"Saved {out}")


def convert_ndvi(folder):
    path_10m = Path(folder) / "response_10m.tiff"
    # NDVI = (NIR - RED) / (NIR + RED) = (B08 - B04) / (B08 + B04)
    compute_index_single(folder, path_10m, band_a_idx=4, band_b_idx=3, name="ndvi", cmap="RdYlGn")


# --- wskaźniki łączące 10m + 20m: NDMI, NBR ---

def compute_index_multi(folder, band_a_10m_idx=None, band_a_20m_idx=None,
                          band_b_10m_idx=None, band_b_20m_idx=None,
                          name="index", cmap="RdYlGn"):
    path_10m = Path(folder) / "response_10m.tiff"
    path_20m = Path(folder) / "response_20m.tiff"

    with rasterio.open(str(path_10m)) as src:
        target_shape = (src.height, src.width)

    def get_band(idx_10m, idx_20m):
        if idx_10m is not None:
            with rasterio.open(str(path_10m)) as src:
                return src.read(idx_10m).astype(np.float32)
        return read_resampled_band(path_20m, idx_20m, target_shape)

    band_a = get_band(band_a_10m_idx, band_a_20m_idx)
    band_b = get_band(band_b_10m_idx, band_b_20m_idx)

    denom = band_a + band_b
    denom[denom == 0] = 1e-6
    index = (band_a - band_b) / denom

    print(f"{name}: min={index.min():.3f}, max={index.max():.3f}, mean={index.mean():.3f}")
    vmin, vmax = np.percentile(index, (2, 98))

    out = output_path_for(folder, name)
    plt.imsave(str(out), index, cmap=cmap, vmin=vmin, vmax=vmax)
    print(f"Saved {out}")


def convert_ndmi(folder):
    # NDMI = (NIR - SWIR1) / (NIR + SWIR1) = (B08 - B11) / (B08 + B11)
    compute_index_multi(folder, band_a_10m_idx=4, band_b_20m_idx=5, name="ndmi", cmap="BrBG")


def convert_nbr(folder):
    # NBR = (NIR - SWIR2) / (NIR + SWIR2) = (B08 - B12) / (B08 + B12)
    compute_index_multi(folder, band_a_10m_idx=4, band_b_20m_idx=6, name="nbr", cmap="RdYlGn")


# --- kompozycje RGB łączące 10m + 20m: SWIR/Agriculture, Urban/Geology ---

def convert_composite_multi(folder, band_specs, name):
    path_10m = Path(folder) / "response_10m.tiff"
    path_20m = Path(folder) / "response_20m.tiff"

    with rasterio.open(str(path_10m)) as src:
        target_shape = (src.height, src.width)

    channels = []
    for idx, res in band_specs:
        if res == "10m":
            with rasterio.open(str(path_10m)) as src:
                channels.append(src.read(idx).astype(np.float32))
        else:
            channels.append(read_resampled_band(path_20m, idx, target_shape))

    rgb = np.dstack(channels)
    rgb_norm = np.dstack([normalize(rgb[:, :, i]) for i in range(3)])

    out = output_path_for(folder, name)
    Image.fromarray(rgb_norm).save(str(out))
    print(f"Saved {out}")


def convert_swir_agriculture(folder):
    # R=B11(20m), G=B08(10m), B=B02(10m)
    convert_composite_multi(folder, [(5, "20m"), (4, "10m"), (1, "10m")], "swir_agriculture")


def convert_urban_geology(folder):
    # R=B12(20m), G=B11(20m), B=B04(10m)
    convert_composite_multi(folder, [(6, "20m"), (5, "20m"), (3, "10m")], "urban_geology")


# --- dispatcher ---

def convert_image(folder, outs):
    if "N" in outs:
        convert_ndvi(folder)
    if "T" in outs:
        convert_true_color(folder)
    if "F" in outs:
        convert_false_color(folder)
    if "M" in outs:
        convert_ndmi(folder)
    if "B" in outs:
        convert_nbr(folder)
    if "S" in outs:
        convert_swir_agriculture(folder)
    if "U" in outs:
        convert_urban_geology(folder)


def convert_images(folder, outs):
    if folder is not None:
        convert_image(folder, outs)
        return

    base = Path("data/raw")
    for scene_folder in os.listdir(base):
        convert_image(str(base / scene_folder), outs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts raster files to png files")
    parser.add_argument("-i", "--input", required=False, help="input scene folder (contains response_10m.tiff / response_20m.tiff)")
    parser.add_argument("-o", "--output", required=True,
                         help="which outputs to generate: T=true color, F=false color, N=ndvi, M=ndmi, B=nbr, S=swir/agri, U=urban/geology")

    args = parser.parse_args()
    convert_images(args.input, args.output)