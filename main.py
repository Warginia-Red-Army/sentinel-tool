import argparse
import calendar
import os
from datetime import date

from database.database import init_database
from tools import locations, download

from sentinelhub import (
    CRS,
    BBox
)

import bbox_helper
import download_map

# def download():
#     today = date.today()
#     end_year = today.year
#
#     os.makedirs("output", exist_ok=True)
#
#     for year in range(end_year - 10, end_year + 1):
#         for month in range(5, 9):
#             month_start = date(year, month, 1)
#             if month_start > today:
#                 continue  # skip future months
#
#             last_day = calendar.monthrange(year, month)[1]
#             month_end = date(year, month, last_day)
#             if month_end > today:
#                 month_end = today
#
#             time_interval = (month_start.isoformat(), month_end.isoformat())
#
#             bbox = BBox(bbox_helper.convertToCorrectBbox(bbox_helper.osielsko), crs=CRS.WGS84)
#             download_map.download(time_interval, bbox)

def tools(tool):
    if tool is None or tool == "":
        parser.print_help("Need type of tool")
        return

    print(f"using tool {tool}")

def set_location():
    pass

def open_location():
    pass

def main():
    parser = argparse.ArgumentParser(
        description="Download and convert Sentinel-2 imagery"
    )

    tools = parser.add_subparsers(
        dest="tool",
        title="Tools",
        required=True
    )

    locations.register_parser(tools)
    download.register_parser(tools)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    init_database()
    main()
    # parser = argparse.ArgumentParser(description="Sentinel Hub Downloader")
    # tools = parser.add_subparsers(dest="tool")
    # convert = tools.add_parser("convert")
    # convert.add_argument("--input", required=True)
    # download = tools.add_parser("download")
    # # download.add_argument("-l", "--location", required=False)
    # download.add_argument("-al", "--availablelocations", required=False, action="store_true")
    # location = tools.add_parser("location")
    # args = parser.parse_args()
    # if args.tool == "convert":
    #     print("converting: ", args.input)
    # if args.tool == "location":
    #     pass
    # else:
    #     print("downloading: ", args.url)
    # print(args.tool == "convert")