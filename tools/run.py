from shlex import shlex
from time import sleep

from main import create_parser
from utility.progress import progress


def register_parser(tools):
    parser = tools.add_parser("run")
    parser.set_defaults(func=run)

def run(args):
    parser = create_parser()
    while True:
        try:
            command = input("> ")
            if command in ("exit", "quit"):
                break

            if not command.strip():
                continue

            command_args = parser.parse_args(shlex.split(command))

            if hasattr(command_args, "func"):
                command_args.func(command_args)

        except SystemExit:
            pass
        except KeyboardInterrupt:
            print("\nExiting...")
            break