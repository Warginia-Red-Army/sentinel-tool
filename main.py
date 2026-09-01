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

print("Gotowe.")