import mysql.connector


class TableBlueprint:
    def __init__(self, name: str, attributes: dict[str, str] = None) -> None:
        self.name = name
        self._attributes = attributes if attributes is not None else {}

    def add_attribute(self, name: str, type: str) -> None:
        self._attributes[name] = type

    def remove_attribute(self, name: str) -> None:
        self._attributes.pop(name)

    @property
    def attributes(self) -> dict:
        return self._attributes

    def get_attribute_type(self, name: str) -> type:
        return self._attributes[name]
    
    def get_attribute_name(self, type: str) -> list[str]:
        names = []
        for (name, attr_type) in self._attributes.items():
            if attr_type == type:
                names.append(name)
        return names

    def __str__(self) -> str:
        return f"Table(name={self.name}, attributes={self.attributes})"

    def __repr__(self) -> str:
        return str(self)


class TableBlueprintMaker:
    def __init__(self, config: dict, cursor) -> None:
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()
        self.config = config

    def get_table_blueprint(self, table_name: str) -> TableBlueprint:
        self.cursor.execute(self._get_column_query(table_name))
        columns = self.cursor.fetchall()
        table_blueprint = TableBlueprint(table_name)
        for column in columns:
            table_blueprint.add_attribute(column[0], column[1])
        return table_blueprint

    def _get_column_query(self, table_name: str):
        return f"""SELECT COLUMN_NAME, DATA_TYPE
                   FROM information_schema.COLUMNS
                   WHERE TABLE_SCHEMA = '{self.config['database']}' 
                         AND TABLE_NAME = '{table_name}'"""
    

class DatabaseBlueprintMaker:
    def __init__(self, config: dict) -> None:
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()
        self.maker = TableBlueprintMaker(config, self.cursor)
        self.config = config
    
    def get_database_blueprint(self) -> list[TableBlueprint]:
        blueprints: list[TableBlueprint] = []

        self.cursor.execute(self._get_table_query())
        tables = self.cursor.fetchall()

        for table in tables:
            blueprints.append(self.maker.get_table_blueprint(table[0]))
        return blueprints

    def close(self):
        self.cursor.close()
        self.connection.close()

    def _get_table_query(self):
        return f"""SELECT TABLE_NAME
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = '{self.config['database']}'"""
