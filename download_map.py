from sentinelhub import (
    SHConfig,
    SentinelHubRequest,
    SentinelHubCatalog,
    DataCollection,
    MimeType,
    CRS,
    BBox
)
from dotenv import load_dotenv
import os
from datetime import date
import calendar
import fix_output
# from main import catalog

load_dotenv(verbose=True)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not client_id:
    raise ValueError("CLIENT_ID not found in .env")
if not client_secret:
    raise ValueError("CLIENT_SECRET not found in .env")

config = SHConfig()
config.sh_client_id = client_id
config.sh_client_secret = client_secret
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

data_collection = DataCollection.SENTINEL2_L2A.define_from(
    "s2l2a_cdse", service_url="https://sh.dataspace.copernicus.eu"
)

catalog = SentinelHubCatalog(config=config)

evalscript_10m = """
//VERSION=3
function setup() {
    return {
        input: ["B02", "B03", "B04", "B08"],
        output: { bands: 4, sampleType: "FLOAT32" }
    };
}
function evaluatePixel(sample) {
    return [sample.B02, sample.B03, sample.B04, sample.B08];
}
"""

evalscript_20m = """
//VERSION=3
function setup() {
    return {
        input: ["B05", "B06", "B07", "B8A", "B11", "B12"],
        output: { bands: 6, sampleType: "FLOAT32" }
    };
}
function evaluatePixel(sample) {
    return [sample.B05, sample.B06, sample.B07, sample.B8A, sample.B11, sample.B12];
}
"""


def save(bbox: BBox, scene_date, base_name):
    request_bands = SentinelHubRequest(
        evalscript=evalscript_10m,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=data_collection,
                time_interval=(scene_date, scene_date)
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=(1000, 1000),
        config=config,
        data_folder=f"cache/raw/rgb"
    )
    request_bands.get_data(save_data=True)

    saved_files = request_bands.get_filename_list()
    if saved_files:
        fix_output.fix_path(request_bands.data_folder, saved_files, base_name)


def download(time_interval: (date, date), bbox: BBox):
    search = catalog.search(
        data_collection,
        bbox=bbox,
        time=time_interval,
        filter="eo:cloud_cover < 60"  # loose filter; tighten if needed
    )

    results = list(search)

    if not results:
        print(f"{time_interval[0]}:{time_interval[1]} no results")
        return
    best_item = min(
        results,
        key=lambda item: item["properties"].get("eo:cloud_cover", 100)
    )

    # for item in results:
    #     print(
    #         item
    #     )

    print(best_item)
    print(f"Items: {len(results)}")

    scene_date = best_item["properties"]["datetime"][:16]
    cloud = best_item["properties"].get("eo:cloud_cover")

    # print(f"{year}-{month:02d}: {scene_date} (clouds: {cloud}%)")
    base_name = f"{scene_date.replace("T", "_").replace(":", "_")}"
    print(f"Best item: {base_name} {cloud}%")
    save(bbox, scene_date[:10], base_name)

    # # --- RGB download ---
    # request_rgb = SentinelHubRequest(
    #     evalscript=evalscript_10m,
    #     input_data=[
    #         SentinelHubRequest.input_data(
    #             data_collection=data_collection,
    #             time_interval=(scene_date, scene_date)
    #         )
    #     ],
    #     responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    #     bbox=bbox,
    #     size=(1000, 1000),
    #     config=config,
    #     data_folder=f"cache/raw/rgb"
    # )
    # request_rgb.get_data(save_data=True)

    # saved_files = request_rgb.get_filename_list()
    # if saved_files:
    #     fix_output.fix_path(request_rgb.data_folder, saved_files, base_name)

    print("Ready")
