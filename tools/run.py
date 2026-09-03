from main import create_parser


def register_parser(tools):
    parser = tools.add_parser("run")
    parser.set_defaults(func=run)

def run(args):
    parser = create_parser()
    while True:
        try:
            command = input("> ")
            if command == "exit":
                break

            if not command.strip():
                continue

            command_args = parser.parse_args(command.split())

            if hasattr(command_args, "func"):
                command_args.func(command_args)

        except SystemExit:
            pass
        except KeyboardInterrupt:
            print("\nExiting...")
            break