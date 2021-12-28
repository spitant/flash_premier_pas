# -*- coding: utf-8 -*-
"""Test unitaire"""
import random
from string import ascii_lowercase

import pytest

from projet.routes import app
from projet.tools.init_db import init_database


@pytest.fixture(scope="session", autouse=True)
def auto_setup(request):
    """
    Mise en place de l'environnement de test
    :param request:
    :return:None
    """
    print("auto_setup")
    init_database()

    def auto_teardown():
        """
        Netoyage de l'environnement
        :return: None
        """
        print("auto_teardown")

    request.addfinalizer(auto_teardown)


def random_string(size=6, chars=ascii_lowercase):
    """
    Generation de chaine de caractère aléatoire
    :param size: taille de la chaine de caractères
    :param chars: liste des caractères
    :return: chaine de caractère aléatoire
    """
    return "".join(random.choice(chars) for _ in range(size))  # nosec


def list_routes(method):
    """
    Retourne la liste des routes définit pour une méthode donnée
    :param method: méthode http (GET, PUT, ...)
    :return: la liste des routes définit pour une méthode donnée
    """
    rules = []
    for rule in app.url_map.iter_rules():
        if "static" not in rule.endpoint and method in rule.methods:
            rules.append(str(rule))
    return rules


def test_url_badmethod():
    """
    Test les urls avec une méthode non adaptée.
    Le résultat attendu est une réponse 405.
    :return: None
    """
    put_list = list_routes("PUT")
    for url in list_routes("GET"):
        # on verifie que les URL sans parametres...
        if "<" not in url and ">" not in url:
            if url not in put_list:
                response = app.test_client().put(url)
                assert (
                    response.status_code == 405
                )  # nosec  # Method not allowed


def test_url_ok():
    """
    Test les urls avec une méthode adaptée.
    Le résultat attendu est une réponse 200.
    :return: None
    """
    for url in list_routes("GET"):
        # on verifie que les URL sans parametres...
        if "<" not in url and ">" not in url:
            response = app.test_client().get(url, follow_redirects=True)
            assert response.status_code == 200  # nosec # OK
        # assert response.data == b'Hello, World!'


def test_url_ko():
    """
    Test des url qui ne sont pas défini.
    Le résultat attendu est une réponse 404.
    :return: None
    """
    nb_test_ko = 20
    for _ in range(0, nb_test_ko):
        url = random_string()
        while url in list_routes("GET"):
            url = random_string()
        response = app.test_client().get(url)
        assert response.status_code == 404  # nosec # Not found
