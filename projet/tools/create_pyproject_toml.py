# -*- coding: utf-8 -*-
"""Generation du fichier pyproject.toml pour la création du package"""
from os.path import abspath
from os.path import dirname
from os.path import join

BASE_DIR = join(dirname(abspath(__file__)), "..", "..")
REQUIREMENTS_TXT = join(BASE_DIR, "requirements.txt")
PYPROJECT_TOML = join(BASE_DIR, "pyproject.toml")


def get_requirements():
    """
    Obtenir la liste de toutes les dépences
    :return: la liste de toutes les dépences
    """
    requirements = []
    with open(REQUIREMENTS_TXT, encoding="utf-8") as frequirements:
        for requirement_line in frequirements.readlines():
            requirement_line = requirement_line.strip()
            if not requirement_line.startswith("#"):
                if "#" in requirement_line:
                    requirement_line = requirement_line.split("#")[0]
                if requirement_line:
                    requirements.append(requirement_line)
    return requirements


if __name__ == "__main__":
    with open(PYPROJECT_TOML, "w", encoding="utf-8") as f:
        f.write("[build-system]\n")
        f.write("requires = [\n")
        for requirement in get_requirements():
            f.write(f'\t"{requirement}",\n')
        f.write("]\n")
        f.write('build-backend = "setuptools.build_meta"\n')
