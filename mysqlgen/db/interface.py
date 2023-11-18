from mysqlgen.db import blueprint
import mysqlgen.stream.serializer as serializer
import mysqlgen.db.maker as maker
import mysqlgen.db.generator as generator
import mysqlgen.db.connector.injector as connectorInjector
import mysql.connector


class DBInterface:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database
        self.serializer = serializer.DatabaseTypeSerializer()

        self.connection = mysql.connector.connect(user=self.user,
                                                  password=self.password,
                                                  host=self.host,
                                                  database=self.database_name,
                                                  raise_on_warnings=True)
        self.blueprints = blueprint.DatabaseBlueprintMaker(self._get_config(),
                                                           self.connection.cursor()) \
                                   .get_database_blueprint()
        self.injector = connectorInjector.InjectorOnFly(self.connection.cursor())

    def change_database(self, database_name: str) -> None:
        self.database_name = database_name

    def init(self):
        serializer.DatabaseTypeSerializer().serialize(self.database_name,
                                                     self.blueprints)
        self.update()
        return self
 
    def update(self):
        self.blueprints = serializer.DatabaseTypeDeserializer() \
                                    .deserialize(self.database_name)

    def inject(self, nb_insertions: int):
        self.injector.injectAll(self.blueprints, nb_insertions)

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
