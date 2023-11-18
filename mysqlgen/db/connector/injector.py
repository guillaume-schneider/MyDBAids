import mysql.connector
import mysql_generator_value.db.objects


class Injector:
    def __init__(self, config: dict, connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

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
