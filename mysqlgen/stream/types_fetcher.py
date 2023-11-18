import json
import os
import mysqlgen.properties as proprieties


class TableTypeFetcher:
    @staticmethod
    def fetch(db_name: str, table_name: str) -> dict:
        with open(f"{proprieties.CONFIG_DIRECTORY}/{db_name}/{table_name}", "r") as file:
            return json.load(file)


class DatabaseTypeFetcher:
    @staticmethod
    def fetch(db_name: str) -> list[dict]:
        list_types = []
        for table_name in os.listdir(f"{proprieties.CONFIG_DIRECTORY}/{db_name}"):
            list_types.append(TableTypeFetcher.fetch(db_name, table_name))
        return list_types
