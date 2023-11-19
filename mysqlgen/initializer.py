from mysqlgen.utils.pattern import Singleton
from mysqlgen.stream.blueprint import TableBlueprintSerializer
import properties
import os
import json


class Initializer(metaclass=Singleton):
    def __init__(self):
        self._tables = []
        self._create_directory(properties.CONFIG_DIRECTORY)
        self._create_json_file(TableBlueprintSerializer.DEFAULT_FILE_TYPE, 
                               TableBlueprintSerializer.DEFAULT_TYPE_MATCH)

    def _create_directory(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _create_json_file(self, file: str, data) -> None:
        if not os.path.exists(file):
            with(open(file, "w")) as f:
                json.dump(data, f, indent=4)
