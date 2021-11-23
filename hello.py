"""Fichier principal de l'application (temporaire: il faut que je reorganise tout ça...)"""
import sqlite3
from os.path import dirname, abspath, join

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

BASE_DIR = dirname(abspath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


def get_db_connection():
    db_path = join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post_data = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post_data is None:
        abort(404)
    return post_data


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<int:post_id>')
def post(post_id):
    return render_template('index.html', posts=[get_post(post_id)])


@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=get_post(post_id))


@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post_request = get_post(post_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post_request['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
