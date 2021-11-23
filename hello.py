"""Fichier principal de l'application (temporaire: il faut que je reorganise tout ça...)"""
from os.path import join, abspath, dirname

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from tools.database_utils import open_database, insert_post, close_database, getall_post, \
    delete_post, getone_post, \
    update_post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/create', methods=('GET', 'POST'))
def create():
    """
    Création d'un nouvel article
    :return: La page de création d'un nouvel article
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = open_database()
            insert_post(connection, title, content)
            close_database(connection)
            return redirect(url_for('index'))

    return render_template('create.html')


def get_post(post_id, markdown_enable=True):
    """
    Récupération d'un article spécifique
    :param post_id: Identifiant de l'article
    :param markdown_enable: activation du markdown
    :return: Article correspondant
    """
    connection = open_database()
    post_data = getone_post(connection, post_id, markdown_enable)
    close_database(connection)
    if post_data is None:
        abort(404)
    return post_data


@app.route('/')
def index():
    """
    Page d'accueil
    :return: La page d'accueil
    """
    connection = open_database()
    posts = getall_post(connection)
    close_database(connection)
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    """
    Page à propos de ...
    :return: La page à propos de ...
    """
    return render_template('about.html')


@app.route('/todo')
def todo():
    """
    Page des choses à faire
    :return: La page des choses à faire
    """
    current_dir = dirname(abspath(__file__))
    list_todo = []
    list_done = []
    with open(join(current_dir, "TODO.txt"), encoding='UTF-8') as todo_file:
        for line in todo_file.readlines():
            if len(line.split(';')) >= 2:
                status = line.split(';')[0]
                if status == "DONE":
                    list_done.append(line.split(';')[1])
                if status == "TODO":
                    list_todo.append(line.split(';')[1])
    done = len(list_done)
    total = len(list_todo) + done
    stat = f'{done}/{total}'
    return render_template('todo.html', list_todo=list_todo, list_done=list_done, stat=stat)


@app.route('/<int:post_id>')
def post(post_id):
    """
    Affichage d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    return render_template('index.html', posts=[get_post(post_id)])


@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    """
    Edition d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Un titre est requis!')
        else:
            conn = open_database()
            update_post(conn, post_id, title, content)
            close_database(conn)
            return redirect(url_for('index'))

    return render_template('edit.html', post=get_post(post_id, False))


@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    """
    Suppression d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    post_request = get_post(post_id)
    conn = open_database()
    delete_post(conn, post_id)
    close_database(conn)
    titre = post_request['title']
    flash(f'L\'article "{titre}" a été supprimé avec succès!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
