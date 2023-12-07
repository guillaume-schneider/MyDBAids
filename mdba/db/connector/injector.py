import mdba.db.generator as generator
import mdba.db.blueprint as blueprint
import mdba.db.objects as objects


@DeprecationWarning
class Injector:
    def __init__(self, config: dict, cursor) -> None:
        self.cursor = cursor

    def inject(self, database: objects.Database):
        for table in database.tables:
            names = self._get_names_field_str(table)
            values = self._get_values_field_str(table)
            self.cursor.execute(f"INSERT INTO `{table.name}` ({names}) VALUES ({values})")
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
    def __init__(self, connection, cursor) -> None:
        self.connection = connection
        self.cursor = cursor
    
    def injectAll(self, blueprints: list[blueprint.TableBlueprint], nb_insertions: int, order: list[str]):
        sql_request = ""
        for order_table in order:
            for blueprint in blueprints:
                if order_table == blueprint.name:
                    self.cursor.execute(self.get_reset_increment_on_empty_table(blueprint.name))
                    self.cursor.execute(generator.DataGenerator().generate(blueprint, nb_insertions))
        try:
            self.connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {str(e)}")
            self.connection.rollback()

    def injectByTable(self, blueprint: blueprint.TableBlueprint, nb_insertions: int):
        sql_request = self.get_reset_increment_on_empty_table(blueprint.name)
        sql_request += generator.DataGenerator().generate(blueprint, nb_insertions)
        print(sql_request)
        try:
            self.cursor.execute(sql_request)
            self.connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {str(e)}")
            self.connection.rollback()

    def get_reset_increment_on_empty_table(self, table_name: str) -> str:
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        if self.cursor.fetchone()[0] == 0:
            return f"ALTER TABLE `{table_name}` AUTO_INCREMENT = 0;\n"
        return ""
    
    def delete_injected_data(self, blueprints: list[blueprint.TableBlueprint], order: list[str]):
        sql_request = ""
        for order_table in order:
            for blueprint in blueprints:
                if order_table == blueprint.name:
                    self.cursor.execute(f"DELETE FROM `{blueprint.name}`;\n")
        print(sql_request)
        try:
            self.connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {str(e)}")
            self.connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
