import argparse

from database.database import init_database
from cli import locations, download, convert, run

def create_parser():
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
    run.register_parser(tools)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    init_database()
    main()