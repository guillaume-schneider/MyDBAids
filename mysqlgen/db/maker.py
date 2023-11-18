import objects as objects
import generator.stream.types as types


class TableMaker:
    @staticmethod
    def make(table_name: str) -> objects.Table:
        table = objects.Table(types.TableTypeFetcher.fetch(table_name))
        for (name, faker_type) in table.get_types_match().items():
            table.add_datas(name, [])
        return table


class DatabaseMaker:
    @staticmethod
    def make(db_name: str) -> objects.Database:
        database = objects.Database()
        types_list = types.DatabaseTypeFetcher.fetch(db_name)
        for types in types_list:
            table = object.Table(types)
            for (name, faker_type) in types.items():
                table.add_datas(name, [])
                database.add_table(table)
        return database
