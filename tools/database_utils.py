"""Fonctions d'aide pour la manipulation de la base de donnée"""
import sqlite3
from os.path import join, abspath, dirname

DATABASE_FILE = "database.db"
DATABASE_SCHEMA = "schema.sql"
BASE_DIR = dirname(abspath(__file__))


def open_database():
    return sqlite3.connect(join(BASE_DIR, "..", DATABASE_FILE))


def execute_schema(connection):
    with open(join(BASE_DIR, "..", DATABASE_SCHEMA), encoding='UTF-8') as f:
        connection.executescript(f.read())
    connection.commit()


def close_database(connection):
    connection.commit()
    connection.close()


def insert_post(connection, titre, contenu):
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                (titre, contenu))
