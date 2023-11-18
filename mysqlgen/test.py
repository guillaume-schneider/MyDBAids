import mysql.connector
import re

def get_table_order(connection):
    cursor = connection.cursor()

    # Exécutez la requête pour obtenir la liste des tables
    cursor.execute("SHOW TABLES")

    # Obtenez la liste des noms de tables
    tables = [table[0] for table in cursor.fetchall()]

    print("Tables :", tables)
    # Initialisez le graphe des dépendances
    dependency_graph = {}

    for table_name in tables:
        # Exécutez la requête pour obtenir la création complète de la table
        cursor.execute(f"SHOW CREATE TABLE {table_name}")

        # Obtenez la création complète de la table
        create_table_statement = cursor.fetchone()[1]

        # Utilisez une expression régulière pour trouver les clés étrangères
        foreign_keys = re.findall(r'FOREIGN KEY \(`(.*?)`\) REFERENCES `(.*?)`', create_table_statement)

        # Obtenez les tables référencées
        referenced_tables = set(fk[1] for fk in foreign_keys)

        # Ajoutez la table actuelle et ses tables référencées au graphe
        dependency_graph[table_name] = referenced_tables

    # Utilisez le graphe pour déterminer l'ordre de création des tables
    order = topological_sort(dependency_graph)

    return order

def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(node):
        nonlocal visited
        visited.add(node)
        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]

# Connexion à la base de données
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="firefighter"
)

# Obtenez l'ordre de création des tables
table_order = get_table_order(connection)

# Fermez la connexion
connection.close()

# Affichez l'ordre de création des tables
# print("Ordre de création des tables :", table_order)
