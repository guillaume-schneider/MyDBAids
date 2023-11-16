import objects
from utils import Singleton
import faker

class TableGenerator(metaclass=Singleton):
    def __init__(self):
        self._faker = faker.Faker()

    def generate(table: objects.Database, nb_insertions: int):
        pass
