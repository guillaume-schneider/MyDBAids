import random
from typing import Any
import mysqlgen.db.blueprint as blueprint
import mysqlgen.utils as utils
import faker


class DataGenerator(metaclass=utils.Singleton):

    def __init__(self) -> None:
        self.ID_COUNTER = 0
        pass

    def generate(self, blueprint: blueprint.TableBlueprint, nb_insertion: int) -> str:
        self.ID_COUNTER = 0
        names = self._get_names_field_str(blueprint)
        res = f"INSERT INTO {blueprint.name} ({names}) VALUES "
        for i in range(nb_insertion):
            res += f"({self._get_values_field_str(blueprint)}), "    
        res = res[:-2] + ";\n"
        return res

    def _get_values_field_str(self, table: blueprint.TableBlueprint) -> str:
        values = ""
        for (name_attr, type_attr) in table.attributes.items():
            if type_attr == "primary_id":
                generated_data = self.ID_COUNTER
                self.ID_COUNTER += 1
            else:
                generated_data = _DataGeneratorMatcher().generate(type_attr)
            values += f"{generated_data}, "
        return values[:-2]

    def _get_names_field_str(self, table: blueprint.TableBlueprint) -> str:
        names = ""
        for (name_attr, attr_type) in table.attributes.items():
            names += f"{name_attr}, "
        return names[:-2]


class _DataGeneratorMatcher(metaclass=utils.Singleton):
    def __init__(self) -> None:
        self._faker_gen = _FakerDataGenerator()
        self._raw_gen = _RawDataGenerator()

    def generate(self, abstract_data_type: str) -> Any:
        match(abstract_data_type):
            case "float":
                return self._raw_gen.generate("float", (0, 100))
            case "int":
                return self._raw_gen.generate("int", (0, 100))
            case "boolean":
                return self._raw_gen.generate("boolean", None)
            case _:
                return self._faker_gen.generate(abstract_data_type)


class _FakerDataGenerator():
    def __init__(self) -> None:
        self._faker = faker.Faker()

    def generate(self, function: str) -> Any:
        if hasattr(self._faker, function) and callable(getattr(self._faker, function)):
            faker_function = getattr(self._faker, function)

            try:
                result = faker_function()
                if self.isString(function):
                    return f"'{result}'"
                return result
            except Exception as e:
                print(f"Erreur lors de l'appel de la fonction {function}: {e}")
                return None
        else:
            print(f"La fonction {function} n'existe pas dans le module faker.")
            return None

    def isString(self, function: str) -> bool:
        return hasattr(self._faker, function) and callable(getattr(self._faker, function)) and \
               type(getattr(self._faker, function)()) == str


class _RawDataGenerator():
    def __init__(self) -> None:
        pass

    def generate(self, data_type: str, args: tuple[int, int]) -> Any:
        match(data_type):
            case "float":
                return round(self._generate_float(args), 3)
            case "int":
                return random.randint(args[0], args[1])
            case "boolean":
                return random.choice([True, False])

    def _generate_float(self, range: tuple[int, int]) -> float:
        return random.random() * random.randint(range[0], range[1])

    def _generate_int(self, range: tuple[int, int]) -> int:
        return random.randint(range[0], range[1])

    def _generate_boolean(self) -> bool:
        return random.choice([True, False])
