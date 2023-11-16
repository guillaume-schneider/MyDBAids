import blueprint as blueprint
import stream.serializer as serializer
import db.maker as maker
import generator as generator
import connector.injector as injector


class DBInterface:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database
        self.database = None
        self.serializer = serializer.DatabaseTypeSerializer()
        self.blueprints = blueprint.DatabaseBlueprintMaker(self._get_config()) \
                                   .get_database_blueprint()
        self.injector = injector.Injector(self._get_config())
        

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
