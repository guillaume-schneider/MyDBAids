from mysqlgen.utils.pattern import Singleton


class RealTimeCLI(metaclass=Singleton):
    def __init__(self):
        pass

    def run(self, interface):
        while True:
            user_input = input("mysqlgen>")

            if self._is_command_utility(user_input):
                if self._is_exit(user_input):
                    print("Bye !")
                    break

                if self._is_help(user_input):
                    self._print_usage()
                    continue

                if self._is_help_command(user_input):
                    for command in CommandManager().get_commands():
                        if command.match(user_input.split(" ")[1]):
                            command.print_help()
                            break
                    continue
            else:
                for command in CommandManager().get_commands():
                    if command.match(user_input):
                        command.execute(interface, user_input.split(" ")[1:])
                        break
            
    def _is_command_utility(self, command: str) -> bool:
        return self._is_help(command) or self._is_help_command(command) \
               or self._is_exit(command)

    def _is_help(self, command: str) -> bool:
        return (command.lower() == "help" or command.lower() == "quit") \
                and len(command.split(" ")) == 1

    def _is_help_command(self, command: str) -> bool:
        return "help" in command.lower() and len(command.split(" ")) == 2

    def _is_exit(self, command: str) -> bool:
        return "exit" in command.lower() and len(command.split(" ")) == 1

    def _print_usage(self):
        print("Usage :")
        print("help : print this message")
        print("exit : exit the program")


class CommandManager(metaclass=Singleton):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def get_commands(self):
        return self.commands


class Command:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func

    def execute(self, interface, args: list[str]):
        if len(args) == 1 and args[0] == "":
            self.func(interface)
        else:
            self.func(interface, *args)

    def match(self, command: str) -> bool:
        return self.name.lower() == command.split(' ')[0].lower()

    def print_help(self):
        print(f"{self.name} - {self.description}")

    def __repr__(self) -> str:
        return f"{self.name} - {self.description}"
