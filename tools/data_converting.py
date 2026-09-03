from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling


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

def convert_raster(folder, bands=(3, 2, 1)):
    rgb_path = Path(folder) / "response_10m.tiff"
    with rasterio.open(str(rgb_path)) as src:
        red = src.read(bands[0])
        green = src.read(bands[1])
        blue = src.read(bands[2])

    rgb = np.dstack([red, green, blue]).astype(np.float32)
    rgb_norm = np.dstack([normalize(rgb[:, :, i]) for i in range(3)])

    return rgb_norm


def convert_true_color(folder):
    return convert_raster(folder, bands=(3, 2, 1))


def convert_false_color(folder):
    return convert_raster(folder, bands=(4, 3, 2))


def compute_index_single(path_tiff, band_a_idx, band_b_idx):
    with rasterio.open(str(path_tiff)) as src:
        band_a = src.read(band_a_idx).astype(np.float32)
        band_b = src.read(band_b_idx).astype(np.float32)

    denom = band_a + band_b
    denom[denom == 0] = 1e-6
    index = (band_a - band_b) / denom
    return index


def convert_ndvi(folder):
    path_10m = Path(folder) / "response_10m.tiff"
    # NDVI = (NIR - RED) / (NIR + RED) = (B08 - B04) / (B08 + B04)
    return compute_index_single(path_10m, band_a_idx=4, band_b_idx=3)

def compute_index_multi(folder, band_a_10m_idx=None, band_a_20m_idx=None,
                          band_b_10m_idx=None, band_b_20m_idx=None,):
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

    return index


def convert_ndmi(folder):
    # NDMI = (NIR - SWIR1) / (NIR + SWIR1) = (B08 - B11) / (B08 + B11)
    return compute_index_multi(folder, band_a_10m_idx=4, band_b_20m_idx=5)


def convert_nbr(folder):
    # NBR = (NIR - SWIR2) / (NIR + SWIR2) = (B08 - B12) / (B08 + B12)
    return compute_index_multi(folder, band_a_10m_idx=4, band_b_20m_idx=6)


def convert_composite_multi(folder, band_specs):
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

    return rgb_norm

def convert_swir_agriculture(folder):
    # R=B11(20m), G=B08(10m), B=B02(10m)
    return convert_composite_multi(folder, [(5, "20m"), (4, "10m"), (1, "10m")])

def convert_urban_geology(folder):
    # R=B12(20m), G=B11(20m), B=B04(10m)
    return convert_composite_multi(folder, [(6, "20m"), (5, "20m"), (3, "10m")])