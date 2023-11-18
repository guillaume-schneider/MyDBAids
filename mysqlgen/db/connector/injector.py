import mysqlgen.db.generator as generator
import mysqlgen.db.blueprint as blueprint
import mysqlgen.db.objects as objects


@DeprecationWarning
class Injector:
    def __init__(self, config: dict, cursor) -> None:
        self.cursor = cursor

    def inject(self, database: objects.Database):
        for table in database.tables:
            names = self._get_names_field_str(table)
            values = self._get_values_field_str(table)
            self.cursor.execute(f"INSERT INTO {table.name} ({names}) VALUES ({values})")
        self.connection.commit()

    def _get_names_field_str(self, table: objects.Table) -> str:
        names = ""
        for (name, datas) in table.attributes.items():
            names.join(name, ", ")
        return names[:-2]

    def _get_values_field_str(self, table: objects.Table) -> str:
        count = self._get_list_count(table)
        values = ""
        for i in range(count):
            for (name, datas) in table.attributes.items():
                values.join(datas[i], ", ")
        return values

    def _get_list_count(self, table: objects.Table) -> int:
        return table.attributes[0].__len__()


class InjectorOnFly:
    def __init__(self, cursor) -> None:
        self.cursor = cursor
    
    def injectAll(self, blueprints: list[blueprint.TableBlueprint], nb_insertions: int):
        for blueprint in blueprints:
            self.injectByTable(blueprint, nb_insertions)

    def injectByTable(self, blueprint: blueprint.TableBlueprint, nb_insertions: int):
        sql_request = generator.DataGenerator().generate(blueprint, nb_insertions)
        print(sql_request)
        self.cursor.execute(sql_request)
        self.cursor.commit()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
