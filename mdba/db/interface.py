from mdba.db import blueprint
import mdba.stream.blueprint as blueprintSerializer
import mdba.stream.dependency as dependencySerializer
import mdba.db.connector.injector as connectorInjector
import mysql.connector



class DBInterface:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database
        self.serializer = blueprintSerializer.DatabaseBlueprintSerializer()

        self._init()

    def _init(self):
        try:
            self.connection = mysql.connector.connect(user=self.user,
                                                    password=self.password,
                                                    host=self.host,
                                                    database=self.database_name,
                                                    raise_on_warnings=True,
                                                    buffered=True)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Accès refusé. Vérifiez vos informations de connexion.")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("La base de données spécifiée n'existe pas.")
            elif err.errno == 2055:
                print("Erreur de connexion au serveur MySQL. Vérifiez votre configuration réseau.")
            else:
                print(f"Erreur inattendue: {err}")

        self.blueprints = blueprint.DatabaseBlueprintMaker(self._get_config(),
                                                           self.connection.cursor()) \
                                   .get_database_blueprint()
        self.dependency_serializer = dependencySerializer.DependencySerializer(self.connection.cursor(), 
                                                                               self.database_name)
        self.injector = connectorInjector.InjectorOnFly(self.connection,
                                                        self.connection.cursor())

    def change_database(self, database_name: str):
        self.database_name = database_name
        self._init()
        return self._get_database_name()

    def init(self):
        blueprintSerializer.DatabaseBlueprintSerializer().serialize(self.database_name,
                                                                    self.blueprints)
        self.dependency_serializer.serialize()
        self.update()
        return self
 
    def update(self):
        self.blueprints = blueprintSerializer.DatabaseBlueprintDeserializer() \
                                             .deserialize(self.database_name)

    def inject(self, nb_insertions: int):
        order = dependencySerializer.DependencyDeserializer().deserialize_order(self.database_name)
        self.injector.injectAll(self.blueprints, nb_insertions, order)

    def delete_injected_data(self):
        order = dependencySerializer.DependencyDeserializer().deserialize_order(self.database_name)
        self.injector.delete_injected_data(self.blueprints, order)

    def _get_database_name(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DATABASE()")
        current_database = cursor.fetchone()[0]

        cursor.close()
        return current_database

    def _get_config(self):
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database_name,
            'raise_on_warnings': True,
            'max_allowed_packet': 1073741824,
            'connect_timeout': 600
        }
