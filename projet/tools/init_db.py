"""Script de generation de base de données"""
from os.path import exists, join
from os import remove
from shutil import rmtree

from flask_migrate import init, migrate, upgrade

from projet import app, Config


def init_database():
    """
    Création ou Reset de la base de donnée
    :return:
    """
    with app.app_context():
        current_app = app
        migration_dir = current_app.extensions['migrate'].directory
        print(f'Migration dir : {migration_dir}')
        if exists(migration_dir):
            rmtree(migration_dir)
            remove(join(Config.BASE_DIR, Config.DATABASE_FILE))
        init()
        migrate()
        upgrade()


if __name__ == '__main__':
    init_database()
