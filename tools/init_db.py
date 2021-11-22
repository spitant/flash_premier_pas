import sqlite3
from os.path import join, abspath, dirname

DATABASE_FILE="database.db"
DATABASE_SCHEMA="schema.sql"
BASE_DIR = dirname(abspath(__file__))

connection = sqlite3.connect(join(BASE_DIR, "..", DATABASE_FILE))
with open(join(BASE_DIR, "..", DATABASE_SCHEMA)) as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
