import sqlite3
from os.path import join, abspath, dirname
from lorem.text import TextLorem

NB_EXAMPLE = 100
DATABASE_FILE="database.db"
DATABASE_SCHEMA="schema.sql"
BASE_DIR = dirname(abspath(__file__))

connection = sqlite3.connect(join(BASE_DIR, "..", DATABASE_FILE))
with open(join(BASE_DIR, "..", DATABASE_SCHEMA)) as f:
    connection.executescript(f.read())

cur = connection.cursor()
lorem = TextLorem(srange=(1, 3), prange=(30, 100))
for _ in range(0, 100):
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                (lorem.sentence()[:-1], lorem.paragraph()))

connection.commit()
connection.close()
