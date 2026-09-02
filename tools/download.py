
def register_parser(tools):
    parser = tools.add_parser('download',
                              help="Download map data from Sentinel-2")

    parser.add_argument('-l', "--location", required=True)

    parser.set_defaults(func=download)


def download(args):
    print(f"Downloading map data from Sentinel-2: {args.location}")
    print(args)