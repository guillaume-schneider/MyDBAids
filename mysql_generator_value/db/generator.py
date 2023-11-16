import objects
from utils import Singleton
import faker

class TableGenerator(metaclass=Singleton):
    def __init__(self):
        self._faker = faker.Faker()

    def generate(self, table: objects.Table, nb_insertions: int):
        for (name, datas) in table.attributes.items():
            for i in range(nb_insertions):
                table.add_data(name, self._faker.get_value(datas))

class DatabaseTableGenerator:
    @staticmethod
    def generate(database: objects.Database, nb_insertions: int):
        database = objects.Database()
        for table in database.tables:
            TableGenerator.generate(table, nb_insertions)

