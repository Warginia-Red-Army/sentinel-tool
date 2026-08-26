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

import bbox_helper
import download_map
import fix_output
from bbox_helper import bydgoszcz

# load_dotenv(verbose=True)
#
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
#
# if not client_id:
#     raise ValueError("CLIENT_ID nie został znaleziony w .env")
# if not client_secret:
#     raise ValueError("CLIENT_SECRET nie został znaleziony w .env")

# =========================
# SENTINEL HUB CONFIG
# =========================

# config = SHConfig()
# config.sh_client_id = client_id
# config.sh_client_secret = client_secret
# config.sh_base_url = "https://sh.dataspace.copernicus.eu"
# config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
#
# bbox = BBox(
#     bbox=(18.045703178293305, 53.16789106306779, 18.059957683893494, 53.18000404008028),
#     crs=CRS.WGS84
# )
#
# data_collection = DataCollection.SENTINEL2_L2A.define_from(
#     "s2l2a_cdse", service_url="https://sh.dataspace.copernicus.eu"
# )
#
# catalog = SentinelHubCatalog(config=config)

# =========================
# EVALSCRIPTS
# =========================

# evalscript_rgb = """
# //VERSION=3
# function setup() {
#     return {
#         input: ["B04", "B03", "B02"],
#         output: { bands: 3, sampleType: "AUTO" }
#     };
# }
# function evaluatePixel(sample) {
#     return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
# }
# """
#
# evalscript_bands = """
# //VERSION=3
# function setup() {
#     return {
#         input: ["B04", "B08"],
#         output: { bands: 2, sampleType: "FLOAT32" }
#     };
# }
# function evaluatePixel(sample) {
#     return [sample.B04, sample.B08];
# }
# """

# =========================
# MAIN LOOP: last 10 years, one best scene per month
# =========================

today = date.today()
end_year = today.year

os.makedirs("output", exist_ok=True)

for year in range(end_year - 10, end_year + 1):
    for month in range(5, 9):
        month_start = date(year, month, 1)
        if month_start > today:
            continue  # skip future months

        last_day = calendar.monthrange(year, month)[1]
        month_end = date(year, month, last_day)
        if month_end > today:
            month_end = today

        time_interval = (month_start.isoformat(), month_end.isoformat())

        bbox = BBox(bbox_helper.convertToCorrectBbox(bbox_helper.osielsko), crs=CRS.WGS84)
        download_map.download(time_interval, bbox)
        # search = catalog.search(
        #     data_collection,
        #     bbox=bbox,
        #     time=time_interval,
        #     filter="eo:cloud_cover < 60"  # loose filter; tighten if needed
        # )
        # results = list(search)
        #
        # if not results:
        #     print(f"{year}-{month:02d}: no results")
        #     continue
        #
        # best_item = min(
        #     results,
        #     key=lambda item: item["properties"].get("eo:cloud_cover", 100)
        # )
        # scene_date = best_item["properties"]["datetime"][:10]
        # cloud = best_item["properties"].get("eo:cloud_cover")
        #
        # print(f"{year}-{month:02d}: {scene_date} (clouds: {cloud}%)")
        #
        # base_name = f"{year}_{month:02d}_{scene_date}"
        #
        # # --- RGB download ---
        # request_rgb = SentinelHubRequest(
        #     evalscript=evalscript_rgb,
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
        #
        # saved_files = request_rgb.get_filename_list()
        # if saved_files:
        #     fix_output.fix_path(request_rgb.data_folder, saved_files, base_name)
        # request_bands = SentinelHubRequest(
        #     evalscript=evalscript_bands,
        #     input_data=[
        #         SentinelHubRequest.input_data(
        #             data_collection=data_collection,
        #             time_interval=(scene_date, scene_date)
        #         )
        #     ],
        #     responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        #     bbox=bbox,
        #     size=(1000, 1000),
        #     config=config,
        #     data_folder=f"cache/raw/bands"
        # )
        # request_bands.get_data(save_data=True)
        #
        # saved_files = request_bands.get_filename_list()
        # if saved_files:
        #     fix_output.fix_path(request_bands.data_folder, saved_files, base_name)

print("Gotowe.")