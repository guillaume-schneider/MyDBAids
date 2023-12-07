import mysql.connector
import mdba.db.abstract.abstract_type as abstract


class TableBlueprint:
    """Représente le schéma conceptuel d'une table dans une base de données."""
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
    
    def get_attribute_name(self, data_type: str) -> list[str]:
        names = []
        for (name, attr_type) in self._attributes.items():
            if attr_type == data_type:
                names.append(name)
        return names

    def __str__(self) -> str:
        return f"Table(name={self.name}, attributes={self.attributes})"

    def __repr__(self) -> str:
        return str(self)


class TableBlueprintMaker:
    """Classe pour créer un blueprint de table à partir d'une base de données MySQL."""
    def __init__(self, config: dict, cursor) -> None:
        self.cursor = cursor
        self.config = config

    def get_table_blueprint(self, table_name: str) -> TableBlueprint:
        try:
            self.cursor.execute(self._get_column_query(table_name))
        except mysql.connector.Error as err:
            print(f"Erreur lors de la requête SQL pour obtenir les colonnes de la table {table_name}: {err}")

        columns = self.cursor.fetchall()
        table_blueprint = TableBlueprint(table_name)
        for column in columns:
            table_blueprint.add_attribute(column[0], column[1])
    
        self.change_constraint_attribute(table_blueprint)
        return table_blueprint

    def change_constraint_attribute(self, table_blueprint: TableBlueprint) -> None:
        try:
            self.cursor.execute(self._get_constraint_query(table_blueprint.name))
        except mysql.connector.Error as err:
            print(f"Erreur lors de la requête SQL pour obtenir les contraintes de la table {table_blueprint.name}: {err}")

        constraints = self.cursor.fetchall()
        for constraint in constraints:
            if constraint[1] == "PRIMARY":
                table_blueprint.add_attribute(constraint[0], abstract.AbstractType.AUTO_ID.name.lower())
            else:
                table_blueprint.add_attribute(constraint[0], abstract.AbstractType.PRIMARY_ID.name.lower())

    def _get_constraint_query(self, table_name: str):
        return f"""SELECT COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                   FROM information_schema.KEY_COLUMN_USAGE
                   WHERE TABLE_SCHEMA = '{self.config['database']}'
                                        AND TABLE_NAME = '{table_name}';"""

    def _get_column_query(self, table_name: str):
        return f"""SELECT COLUMN_NAME, DATA_TYPE
                   FROM information_schema.COLUMNS
                   WHERE TABLE_SCHEMA = '{self.config['database']}' 
                         AND TABLE_NAME = '{table_name}'"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()


class DatabaseBlueprintMaker:
    """Classe pour créer un blueprint de base de données à partir d'une base de données MySQL."""
    def __init__(self, config: dict, cursor) -> None:
        self.cursor = cursor
        self.maker = TableBlueprintMaker(config, self.cursor)
        self.config = config
    
    def get_database_blueprint(self) -> list[TableBlueprint]:
        blueprints: list[TableBlueprint] = []

        try:
            self.cursor.execute(self._get_table_query())
        except mysql.connector.Error as err:
            print(f"Erreur lors de la requête SQL pour obtenir les tables de la base de données: {err}")      
  
        tables = self.cursor.fetchall()
        for table in tables:
            blueprints.append(self.maker.get_table_blueprint(table[0]))
        return blueprints

    def _get_table_query(self):
        return f"""SELECT TABLE_NAME
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = '{self.config['database']}'"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
