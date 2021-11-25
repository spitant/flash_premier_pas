"""Création de l'instance flask"""
# pylint: skip-file
from os.path import join, abspath, dirname

import markdown
from flask import Flask
from flask_htmlmin import HTMLMIN
from flask_mde import Mde
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class Config():
    """
    Flask configuration
    """
    DATABASE_FILE = "database.db"
    BASE_DIR = join(dirname(abspath(__file__)), "..")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASE_DIR, DATABASE_FILE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'password'
    MINIFY_HTML = True


app = Flask(__name__, template_folder=join(Config.BASE_DIR, "templates"),
            static_folder=join(Config.BASE_DIR, "static"))
app.add_template_global(markdown.markdown, "markdown")

app.config.from_object(Config)
mde = Mde(app)
htmlmin = HTMLMIN(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from projet import routes, models
