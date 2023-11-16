import json
import db.blueprint as blueprint
import utils
import os
import properties


class TableTypeSerializer:
    DEFAULT_FILE_TYPE = f"{properties.CONFIG_DIRECTORY}/types.json"
    DEFAULT_TYPE_MATCH = {
        "varchar": "lorem.paragraph",
        "text": "lorem.paragraph",
        "char": "lorem.paragraph",
        "date": "date_time.date",
        "datetime": "date_time.date",
        "timestamp": "date_time.date_time",
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
        self._types: dict[str, str] = TableTypeSerializer.DEFAULT_TYPE_MATCH

    def serialize(self, db_name: str, blueprint: blueprint.TableBlueprint) -> str:
        if not os.path.exists(f"{properties.CONFIG_DIRECTORY}/{db_name}"):
            os.mkdir(f"{properties.CONFIG_DIRECTORY}/{db_name}")

        self._serialize_types = {}
        self._types = self._get_default_types_match()

        for (name, type) in blueprint.attributes.items():
            self._serialize_types[name] = self._types[type]

        file_path = f"{properties.CONFIG_DIRECTORY}/{db_name}/{blueprint.name}.json"
        if file_path not in os.listdir(properties.CONFIG_TABLES_DIRECTORY):
            self._create_json_file(file_path, self._serialize_types)

        return file_path

    def _get_default_types_match(self):
        with open(TableTypeSerializer.DEFAULT_FILE_TYPE, "r") as f:
            return json.load(f)

    def _create_json_file(self, file: str, data) -> None:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)


class DatabaseTypeSerializer(metaclass=utils.Singleton):
    def __init__(self) -> None:
        self._table_serializer = TableTypeSerializer()

    def serialize(self, db_name: str, blueprints: list[blueprint.TableBlueprint]) -> None:
        for blueprint in blueprints:
            self._table_serializer.serialize(db_name, blueprint)
