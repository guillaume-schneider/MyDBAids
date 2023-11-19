from mysqlgen.utils.function import set_to_dict
from mysqlgen.dependency import constraint_dependency
import json
import mysqlgen.properties as properties
import os
import mysqlgen.utils.pattern as pattern


class DependencySerializer:
    def __init__(self, cursor, db_name) -> None:
        self.db_name = db_name
        self.dependency_path = f"{properties.CONFIG_DIRECTORY}/{self.db_name}/dependency"
        self.order_path = f"{properties.CONFIG_DIRECTORY}/{self.db_name}/order"
        self.table_order_fetcher = constraint_dependency.TableOrderFetcher(cursor)

    def serialize(self) -> None:
        order = self.table_order_fetcher.get_order()
        self._init()
        self._serialize(order,
                        set_to_dict(self.table_order_fetcher.dependency_graph))

    def _init(self):
        if not os.path.exists(self.order_path):
            os.mkdir(self.order_path)
        if not os.path.exists(self.dependency_path):
            os.mkdir(self.dependency_path)

    def _serialize(self, order, dependency):
        self._serialize_order(order)
        self._serialize_dependency(dependency)

    def _serialize_order(self, order: list[str]) -> None:
        order_file_path = f"{self.order_path}/order.json"
        if not os.path.exists(order_file_path):
            with open(order_file_path, "w") as f:
                json.dump(order, f, indent=4)

    def _serialize_dependency(self, dependency: list[str]) -> None:
        dependency_file_path = f"{self.dependency_path}/dependency.json"
        if not os.path.exists(dependency_file_path):
            with open(dependency_file_path, "w") as f:
                json.dump(dependency, f, indent=4)


class DependencyDeserializer(metaclass=pattern.Singleton):
    def __init__(self) -> None:
        pass

    def deserialize_dependency(self, db_name: str) -> list[str]:
        dependency_path = f"{properties.CONFIG_DIRECTORY}/{db_name}/dependency/dependency.json"
        with open(dependency_path, "r") as f:
            return json.load(f)

    def deserialize_order(self, db_name: str) -> list[str]:
        order_path = f"{properties.CONFIG_DIRECTORY}/{db_name}/order/order.json"
        with open(order_path, "r") as f:
            return json.load(f)
