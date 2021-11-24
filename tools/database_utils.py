"""Fonctions d'aide pour la manipulation de la base de donnée"""
import sqlite3
import sys
from os.path import join, abspath, dirname

import markdown

DATABASE_FILE = "database.db"
DATABASE_SCHEMA = "schema.sql"
BASE_DIR = dirname(abspath(__file__))


def open_database():
    """
    Ouvre une base de donnée sqlite et retourne la connection (sous forme d'objet)
    :return: la connection à la base sqlite3 (sous forme d'objet)
    """
    connection = sqlite3.connect(join(BASE_DIR, "..", DATABASE_FILE))
    connection.row_factory = sqlite3.Row
    return connection


def execute_schema(connection):
    """
    Execute un schema sql
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :return: None
    """
    with open(join(BASE_DIR, "..", DATABASE_SCHEMA), encoding='UTF-8') as schema_file:
        connection.executescript(schema_file.read())
    connection.commit()


def close_database(connection):
    """
    Ferme la connection avec la base de donnée
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :return: None
    """
    connection.commit()
    connection.close()


def insert_post(connection, titre, contenu):
    """
    Insertion d'un article dans la base de donnée
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :param titre: titre de l'article à inserer
    :param contenu: contenu de l'article à inserer
    :return: None
    """
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                (titre, contenu))


def getall_post(connection, markdown_enable=True, offset=0, limit=sys.maxsize):
    """
    Récupération de la liste des articles.
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :param markdown_enable: activation du markdown
    :param offset: index de début
    :param  limit: limit max de post
    :return: la liste de tout les articles
    """
    posts = connection.execute('SELECT * FROM posts LIMIT ?,?', (offset, limit,)).fetchall()
    dict_posts = [dict(post) for post in posts]
    if markdown_enable:
        for post in dict_posts:
            post['content'] = markdown.markdown(post['content'])
    return dict_posts


def delete_post(connection, post_id):
    """
    Suppression d'un article
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :param post_id: identifiant de l'article
    :return: None
    """
    connection.execute('DELETE FROM posts WHERE id = ?', (post_id,))


def getone_post(connection, post_id, markdown_enable=True):
    """
    Récupération d'un article.
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :param post_id: identifiant de l'article
    :param markdown_enable: activation du markdown
    :return: L'article correspondant à l'identifiant
    """
    try:
        post = dict(connection.execute('SELECT * FROM posts WHERE id = ?',
                                       (post_id,)).fetchone())
    except TypeError:
        return None
    if markdown_enable:
        post['content'] = markdown.markdown(post['content'])
    return post


def update_post(connection, post_id, titre, contenu):
    """
    Mise à jour d'un article dans la base de donnée
    :param connection: la connection à la base sqlite3 (sous forme d'objet)
    :param post_id: identifiant de l'article
    :param titre: titre du post à mettre à jour
    :param contenu: contenu du post à mettre à jour
    :return: None
    """
    connection.execute('UPDATE posts SET title = ?, content = ?'
                       ' WHERE id = ?',
                       (titre, contenu, post_id))
