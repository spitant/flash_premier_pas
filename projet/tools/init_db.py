# -*- coding: utf-8 -*-
"""Script de generation de base de données"""
from os import remove
from os.path import exists
from os.path import join
from shutil import rmtree

from flask_migrate import init
from flask_migrate import migrate
from flask_migrate import upgrade

from projet import app
from projet import Config


def init_database():
    """
    Création ou Reset de la base de donnée
    :return:
    """
    with app.app_context():
        current_app = app
        migration_dir = current_app.extensions["migrate"].directory
        print(f"Migration dir : {migration_dir}")
        if exists(migration_dir):
            rmtree(migration_dir)
            remove(join(Config.BASE_DIR, Config.DATABASE_FILE))
        init()
        migrate()
        upgrade()


if __name__ == "__main__":
    init_database()
