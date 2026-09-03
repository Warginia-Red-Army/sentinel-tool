import sqlite3
import webbrowser

from database.locations import list_locations, add_location, remove_location, get_location
from file_converting import converters


def register_parser(tools):
    parser = tools.add_parser(
        "location",
        help="Manage locations in database"
    )

    locations = parser.add_subparsers(dest="location_command", required=True)

    # NEW
    new = locations.add_parser(
        "new",
        help="Create new location"
    )
    new.add_argument("-n", "--name")
    new.add_argument("--coordinates", type=float, nargs=4, help="Four coordinate values", metavar=("LAT1", "LON1", "LAT2", "LON2"))

    new.set_defaults(func=new_location)

    # LIST
    list = locations.add_parser(
        "list",
        help="Create new location"
    )

    list.set_defaults(func=list_location)

    # OPEN
    open = locations.add_parser(
        "open",
        help="Open new location"
    )

    open.add_argument("-n", "--name")
    open.set_defaults(func=open_location)


    # REMOVE
    remove = locations.add_parser(
        "remove",
        help="Remove location"
    )
    remove.add_argument("-n", "--name")
    remove.set_defaults(func=rm_location)

    # DEFAULT
    parser.set_defaults(func=location)


def new_location(args):
    name = args.name
    (lat1, lon1, lat2, lon2) = args.coordinates
    if not name:
        input("Locaiton name: ")
    if not args.coordinates:
        lon1 = float(input("Longitude 1: "))
        lat1 = float(input("Latitude 1: "))
        lon2 = float(input("Longitude 2: "))
        lat2 = float(input("Latitude 2: "))
    try:
        add_location(name, lon1, lat1, lon2, lat2)
        print("Location added")
    except sqlite3.IntegrityError:
        print(f"Location '{name}' already exists")

def list_location(args):
    print("listing location")
    print(list_locations())

def rm_location(args):
    print("Removing location")
    remove_location(args.name)

def open_location(args):
    print("Opening location")

    location = get_location(args.name)

    if location is None:
        print("Location not found")
        return
    print(location)
    name, lat1, lon1, lat2,lon2 = location[0]
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    url = f"https://www.google.com/maps/@{center_lat},{center_lon},15z"
    webbrowser.open(url)

def location(args):
    print("do nothing")
    print(list_locations())
