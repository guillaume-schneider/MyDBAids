from mysqlgen.db import blueprint
import mysqlgen.stream.serializer as serializer
import mysqlgen.db.maker as maker
import mysqlgen.db.generator as generator
import mysqlgen.db.connector.injector as injector
import mysql.connector


class DBInterface:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database
        self.database = None
        self.serializer = serializer.DatabaseTypeSerializer()

        self.connection = mysql.connector.connect(user=self.user,
                                                  password=self.password,
                                                  host=self.host,
                                                  database=self.database_name,
                                                  raise_on_warnings=True)
        self.blueprints = blueprint.DatabaseBlueprintMaker(self._get_config(),
                                                           self.connection.cursor()) \
                                   .get_database_blueprint()
        self.injector = injector.Injector(self._get_config(), self.connection.cursor())

    def change_database(self, database_name: str) -> None:
        self.database_name = database_name

    def init(self):
        serializer.DatabaseTypeSerializer().serialize(self.database_name, 
                                                      self.blueprints)
        self.database = maker.DatabaseMaker().make(self.database_name)

    def inject(self, nb_insertions: int):
        generator.DatabaseTableGenerator() \
                 .generate(self.database, nb_insertions)
        self.injector.inject(self.database)

    def delete_injected_data(self):
        pass

    def _get_config(self):
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database_name,
            'raise_on_warnings': True
        }
