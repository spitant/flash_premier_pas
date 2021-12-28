# -*- coding: utf-8 -*-
"""Script de generation de base de données contenant des exemples de postes"""
from lorem.text import TextLorem

from projet import app
from projet import db
from projet.models import Article
from projet.tools.init_db import init_database

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
    text = f"# {titre1}\n"
    text += lorem_generator.paragraph() + lorem_generator.paragraph() + "\n"
    text += f"# {titre2}\n"
    text += f"## {titre21}\n"
    text += lorem_generator.paragraph() + "\n"
    text += f"## {titre22}\n"
    text += lorem_generator.paragraph() + "\n"
    return text


if __name__ == "__main__":
    init_database()
    with app.app_context():
        lorem = TextLorem(srange=(1, 3), prange=(10, 40))
        for _ in range(0, 100):
            art = Article(titre=lorem.sentence()[:-1], contenu=content(lorem))
            db.session.add(art)
            db.session.commit()
