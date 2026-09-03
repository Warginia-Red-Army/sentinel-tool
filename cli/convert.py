

def register_parser(tools):
    parser = tools.add_parser("convert", help="Convert raw tiff to png")
    parser.set_defaults(func=convert)

def convert(args):
    print("Dummy convert")