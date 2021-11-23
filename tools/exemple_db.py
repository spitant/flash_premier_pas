"""Script de generation de base de données contenant des exemples de postes"""
from lorem.text import TextLorem

from database_utils import open_database, execute_schema, close_database, insert_post

NB_EXAMPLE = 100

if __name__ == '__main__':
    connection = open_database()
    execute_schema(connection)
    lorem = TextLorem(srange=(1, 3), prange=(30, 100))
    for _ in range(0, 100):
        insert_post(connection, lorem.sentence()[:-1], lorem.paragraph())
    close_database(connection)
