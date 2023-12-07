from mydbaids.dependency.topologicaL_sort import SortByDetph
import re


class TableOrderFetcher:
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.dependency_graph = None

    def get_order(self) -> list[str]:
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        self.dependency_graph = {}

        for table_name in tables:
            self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_statement = self.cursor.fetchone()[1]
            foreign_keys = re.findall(r'FOREIGN KEY \(`(.*?)`\) REFERENCES `(.*?)`', create_table_statement)
            referenced_tables = set(fk[1] for fk in foreign_keys)
            self.dependency_graph[table_name] = referenced_tables

        order = SortByDetph.sort(self.dependency_graph)

        return order

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
