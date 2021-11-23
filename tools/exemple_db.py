"""Script de generation de base de données contenant des exemples de postes"""
from lorem.text import TextLorem

from database_utils import open_database, execute_schema, close_database, insert_post

NB_EXAMPLE = 100


def content(lorem_generator):
    """
    Generation du contenue de l'article
    :param lorem_generator: TextLorem generation de texte aléatoire
    :return: Contenue d'un article
    """
    titre1 = lorem_generator.sentence()[:-1]
    titre2 = lorem_generator.sentence()[:-1]
    titre21 = lorem_generator.sentence()[:-1]
    titre22 = lorem_generator.sentence()[:-1]
    text = f'# {titre1}\n'
    text += lorem_generator.paragraph() + lorem_generator.paragraph() + '\n'
    text += f'# {titre2}\n'
    text += f'## {titre21}\n'
    text += lorem_generator.paragraph() + '\n'
    text += f'## {titre22}\n'
    text += lorem_generator.paragraph() + '\n'
    return text


if __name__ == '__main__':
    connection = open_database()
    execute_schema(connection)
    lorem = TextLorem(srange=(1, 3), prange=(10, 40))
    for _ in range(0, 100):
        insert_post(connection, lorem.sentence()[:-1], content(lorem))
    close_database(connection)
