import argparse


def connect(args):
    if args.password is None and args.database is None:
        print(f"Connecting to {args.hostname} as user {args.user} without password")
        return;
    if args.database is not None and args.password is not None:
        print(f"Connecting to {args.hostname} as user {args.user} with password {args.password} and database {args.database}")
    if args.database is not None and args.password is None:
        print(f"Connecting to {args.hostname} as user {args.user} without password and database {args.database}")
    else:
        print(f"Connecting to {args.hostname} as user {args.user} with password {args.password}")

class ConnectorCLI:
    def __init__(self) -> None:
        self.user: str = None
        self.password: str = None
        self.host: str = None
        self.database: str = None

    def connect(self, argv: list[str] = None):
        parser = argparse.ArgumentParser(description="Your CLI description")

        # Connect command (mandatory)
        connect_parser = parser.add_argument_group("Connect Command")
        connect_parser.add_argument("--user", "-u", required=True, help="Username")
        connect_parser.add_argument("--hostname", "-hn", required=True, help="Hostname")
        connect_parser.add_argument("--password", "-p", help="Password")
        connect_parser.add_argument("--database", "-db", help="Database name")
        connect_parser.set_defaults(func=connect)
        args = parser.parse_args(argv if argv else None)

        # Check if connect command is provided
        if not hasattr(args, "func"):
            parser.error("You must provide a command. Use --help for more information.")
        args.func(args)

        self.inject_args(args)
        return args

    def inject_args(self, args):
        self.user = args.user
        self.password = args.password
        self.host = args.hostname
        self.database = args.database
