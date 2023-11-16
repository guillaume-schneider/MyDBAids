import json
import os


class TableTypeFetcher:
    @staticmethod
    def fetch(db_name: str, table_name: str) -> dict:
        with open(f"blueprints/{db_name}/{table_name}.json", "r") as file:
            return json.load(file)


class DatabaseTypeFetcher:
    @staticmethod
    def fetch(db_name: str) -> list[dict]:
        list_types = []
        for table_name in os.listdir(f"blueprints/{db_name}"):
            list_types.append(TableTypeFetcher.fetch(db_name, table_name))
