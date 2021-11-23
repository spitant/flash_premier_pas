"""Script de generation de base de données"""
from database_utils import open_database, execute_schema, close_database

if __name__ == '__main__':
    connection = open_database()
    execute_schema(connection)
    close_database(connection)
