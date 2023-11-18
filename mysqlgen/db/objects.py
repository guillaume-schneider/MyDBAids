@DeprecationWarning
class Table:
    def __init__(self, types_match: dict) -> None:
        self._types_match = types_match
        self.attributes: dict[str, list] = {}

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

    def get_types_match(self):
        return self._types_match

    def __str__(self) -> str:
        return f"Table(attributes={self.attributes})"
    
    def __repr__(self) -> str:
        return str(self)


@DeprecationWarning
class Database:
    def __init__(self, tables: list[Table] = None) -> None:
        self._tables = tables if tables is not None else []

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
