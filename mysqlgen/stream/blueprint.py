import json
import mysqlgen.db.blueprint as blueprint
from mysqlgen.utils.pattern import Singleton
import os
import mysqlgen.properties as properties
from mysqlgen.utils import function


class TableBlueprintSerializer:
    DEFAULT_FILE_TYPE = f"{properties.CONFIG_DIRECTORY}/types.json"
    DEFAULT_TYPE_MATCH = {
        "varchar": "paragraph",
        "text": "paragraph",
        "char": "paragraph",
        "date": "date",
        "datetime": "date",
        "timestamp": "date",
        "decimal": "float",
        "double": "float",
        "float": "float",
        "tinyint": "boolean",
        "smallint": "int",
        "mediumint": "int",
        "int": "int",
        "bigint": "int",
        "year": "int",
    }

    def __init__(self) -> None:
        self._types: dict[str, str] = TableBlueprintSerializer.DEFAULT_TYPE_MATCH

    def serialize(self, db_name: str, blueprint: blueprint.TableBlueprint) -> str:
        db_path = f"{properties.CONFIG_DIRECTORY}/{db_name}"
        if not os.path.exists(db_path):
            os.mkdir(db_path)

        self._serialize_types = {}
        self._types = self._get_default_types_match()

        for (name, type) in blueprint.attributes.items():
            self._serialize_types[name] = self._types[type]

        file_path = f"{db_path}/{blueprint.name}.json"
        if file_path not in os.listdir(db_path):
            self._create_json_file(file_path, self._serialize_types)

        return file_path

    def _get_default_types_match(self):
        with open(TableBlueprintSerializer.DEFAULT_FILE_TYPE, "r") as f:
            return json.load(f)

    def _create_json_file(self, file: str, data) -> None:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)


class DatabaseBlueprintSerializer(metaclass=Singleton):
    def __init__(self) -> None:
        self._table_serializer = TableBlueprintSerializer()

    def serialize(self, db_name: str, blueprints: list[blueprint.TableBlueprint]) -> None:
        for blueprint in blueprints:
            self._table_serializer.serialize(db_name, blueprint)


class TableBlueprintDeserializer:
    def __init__(self) -> None:
        pass

    def deserialize(self, file: str) -> blueprint.TableBlueprint:
        attributes: dict
        with open(file, "r") as f:
            attributes = json.load(f)
        return blueprint.TableBlueprint(file.split("/")[-1].split(".")[0], attributes)


class DatabaseBlueprintDeserializer(metaclass=Singleton):
    def __init__(self) -> None:
        self._table_deserializer = TableBlueprintDeserializer()

    def deserialize(self, db_name: str) -> list[blueprint.TableBlueprint]:
        db_path = f"{properties.CONFIG_DIRECTORY}/{db_name}"
        files = function.get_json_files_in_dir(db_path)
        res: list[blueprint.TableBlueprint] = []
        for file in files:
            res.append(self._table_deserializer.deserialize(f"{db_path}/{file}"))
        return res
