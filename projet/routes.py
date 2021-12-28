# -*- coding: utf-8 -*-
"""Fichier principal de l'application"""
from os.path import abspath
from os.path import dirname
from os.path import join

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from projet import app
from projet import db
from projet.models import Article

ROWS_PER_PAGE = 5


@app.route("/create", methods=("GET", "POST"))
def create():
    """
    Création d'un nouvel article
    :return: La page de création d'un nouvel article
    """
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Un titre est requis!")
        else:
            art = Article(titre=title, contenu=content)
            db.session.add(art)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("create.html")


def get_post(post_id):
    """
    Récupération d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    post_data = Article.query.filter_by(id=post_id).first()
    if post_data is None:
        abort(404)
    return post_data


@app.route("/", methods=["GET"])
def index():
    """
    Page d'accueil
    :return: La page d'accueil
    """
    # récupération de la page
    try:
        page = int(request.args.get("page"))
    except ValueError:
        return redirect(url_for("index", page=1))
    except TypeError:
        return redirect(url_for("index", page=1))
    posts = db.session.query(Article).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    """
    Page à propos de ...
    :return: La page à propos de ...
    """
    return render_template("about.html")


@app.route("/todo")
def todo():
    """
    Page des choses à faire
    :return: La page des choses à faire
    """
    current_dir = dirname(abspath(__file__))
    list_todo = []
    list_done = []
    with open(join(current_dir, "../TODO.txt"), encoding="UTF-8") as todo_file:
        for line in todo_file.readlines():
            if len(line.split(";")) >= 2:
                status = line.split(";")[0]
                if status == "DONE":
                    list_done.append(line.split(";")[1])
                if status == "TODO":
                    list_todo.append(line.split(";")[1])
    done = len(list_done)
    total = len(list_todo) + done
    stat = f"{done}/{total}"
    return render_template(
        "todo.html",
        list_todo=list_todo,
        list_done=list_done,
        stat=stat,
    )


@app.route("/<int:post_id>")
def post(post_id):
    """
    Affichage d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    posts = Article.query.filter_by(id=post_id).paginate(page=1, per_page=ROWS_PER_PAGE)
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    """
    Edition d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Un titre est requis!")
        else:
            article = Article.query.filter_by(id=post_id).first()
            article.titre = title
            article.contenue = content
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("edit.html", post=get_post(post_id))


@app.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    """
    Suppression d'un article spécifique
    :param post_id: Identifiant de l'article
    :return: Article correspondant
    """
    Article.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash("L'article a été supprimé avec succès!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
