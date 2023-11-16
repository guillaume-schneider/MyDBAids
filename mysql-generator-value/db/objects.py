import db.blueprint as blueprint


class Table:
    def __init__(self) -> None:
        attributes: dict[str, list] = {}

    def add_datas(self, name: str, data: list) -> None:
        self.attributes[name] = data

    def remove_datas(self, name: str) -> None:
        self.attributes.pop(name)

    def add_data(self, name: str, data: object) -> None:
        self.attributes[name].append(data)
    
    def remove_data(self, name: str, data: object) -> None:
        self.attributes[name].remove(data)

    def get_datas(self, name: str) -> list:
        return self.attributes[name]

    def get_data(self, name: str, index: int) -> object:
        return self.attributes[name][index]

    def has_data(self, name: str, data: object) -> bool:
        return data in self.attributes[name]

    def __str__(self) -> str:
        return f"Table(attributes={self.attributes})"
    
    def __repr__(self) -> str:
        return str(self)


class TableMaker:
    @staticmethod
    def make(blueprint: blueprint.TableBlueprint) -> Table:
        table = Table()
        for (name, type) in blueprint.attributes.items():
            attributes: list[type] = []
            table.add_datas(name, attributes)
        return table


class Database:
    def __init__(self, tables: list[Table]) -> None:
        self._tables = tables

    def add_table(self, table: Table) -> None:
        self._tables.append(table)

    def get_table(self, name: str) -> Table:
        for table in self._tables:
            if table.name == name:
                return table
        return None

    def remove_table(self, name: str) -> None:
        for table in self._tables:
            if table.name == name:
                self._tables.remove(table)

    def __str__(self) -> str:
        return f"Database(tables={self.tables})"

    def __repr__(self) -> str:
        return str(self)
