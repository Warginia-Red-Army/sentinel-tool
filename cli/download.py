import calendar
import os
from datetime import date

from sentinelhub import (
    CRS,
    BBox
)

from database.locations import get_location
from tools import download_map
from utility import bbox_helper


def register_parser(tools):
    parser = tools.add_parser('download',
                              help="Download location data from Sentinel-2")

    parser.add_argument('-l', "--location", required=True)

    parser.set_defaults(func=download_input)

# downlaod logic
# since year
# until year
# photos in month count
# month/day/week/year interval

def process_download():
    pass

def process_year():
    pass

def process_month():
    pass

def process_day():
    pass

def download_input(args):
    location = args.location
    if not location:
        location = input("Location: ")
    start_year = input("Start year: ")
    end_year = input("End year: ")
    start_month = input("Start month: ")
    end_month = input("End month: ")

    coordinates = get_location(location)
    bbox = BBox(bbox_helper.concert_to_bbox(coordinates), crs=CRS.WGS84)

    download(start_year, end_year, start_month, end_month, bbox)


def download(start_year, end_year, start_month, end_month, bbox):
    today = date.today()
    os.makedirs("output", exist_ok=True)

    for year in range(start_year, end_year):
        for month in range(start_month, end_month):
            month_start = date(year, month, 1)
            if month_start > today:
                continue  # skip future monthssa

            last_day = calendar.monthrange(year, month)[1]
            month_end = date(year, month, last_day)
            if month_end > today:
                month_end = today

            time_interval = (month_start.isoformat(), month_end.isoformat())
            download_map.download(time_interval, bbox)