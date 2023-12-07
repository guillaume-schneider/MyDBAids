from mydbaids.utils.pattern import Singleton
from mydbaids.stream.blueprint import TableBlueprintSerializer
import mydbaids.cli.scripting as scripting
import mydbaids.cli.script.commands as commands
import properties
import os
import json


class Initializer(metaclass=Singleton):
    def __init__(self):
        self._tables = []
        self._create_directory(properties.CONFIG_DIRECTORY)
        self._create_json_file(TableBlueprintSerializer.DEFAULT_FILE_TYPE, 
                               TableBlueprintSerializer.DEFAULT_TYPE_MATCH)
        self._init_script_commands()

    def _create_directory(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _create_json_file(self, file: str, data) -> None:
        if not os.path.exists(file):
            with(open(file, "w")) as f:
                json.dump(data, f, indent=4)

    def _init_script_commands(self):
        scripting.CommandManager().add_command(scripting.Command("init", 
                                                                 "init <database_name>",
                                                                 commands.init_database))
        scripting.CommandManager().add_command(scripting.Command("inject",
                                                                 "inject <nb_insertions>",
                                                                 commands.inject_data))
        scripting.CommandManager().add_command(scripting.Command("clear",
                                                                 "clear",
                                                                 commands.clear))
        scripting.CommandManager().add_command(scripting.Command("update",
                                                                 "update",
                                                                 commands.update))
        scripting.CommandManager().add_command(scripting.Command("use",
                                                                 "use <database_name>",
                                                                 commands.use_database))
        
