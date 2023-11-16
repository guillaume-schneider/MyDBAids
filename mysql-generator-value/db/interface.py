import db.blueprint as blueprint
import parser.serializer as serializer


class DBInterface:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.serializer = serializer.DatabaseTypeSerializer()
        self.blueprints = blueprint.DatabaseBlueprintMaker(self._get_config()) \
                                   .get_database_blueprint()

    def change_database(self, database: str) -> None:
        self.database = database

    def init(self):
        serializer.DatabaseTypeSerializer().serialize(self.blueprints)

    def inject(self):
        pass

    def delete_injected_data(self):
        pass

    def _get_config(self):
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database,
            'raise_on_warnings': True
        }
