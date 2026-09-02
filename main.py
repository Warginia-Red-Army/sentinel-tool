import argparse

from database.database import init_database
from tools import locations, download, convert


def main():
    parser = argparse.ArgumentParser(
        description="Sentinel-2 Tools hub"
    )

    tools = parser.add_subparsers(
        dest="tool",
        title="Tools",
        required=True
    )

    locations.register_parser(tools)
    download.register_parser(tools)
    convert.register_parser(tools)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    init_database()
    main()