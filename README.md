# 1. Premier pas d'utilisation de flask

Ce projet a été construit avec l'aide des tutoriels suivant : 
- [Comment créer une application web en utilisant Flask en Python 3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-fr)
- [Comment ajouter une authentification à votre application avec Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-fr)
- [Testing our Hello World app](https://riptutorial.com/flask/example/4122/testing-our-hello-world-app)
- [Simple Flask Pagination](https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e)

# 2. Utilisation

## 2.1 Installation des prérequis
    pip install -r requirements.txt

## 2.2 Création de la base de donnée

### 2.2.1 Création de la base de donnée vierge

    python tools/init_db.py

### 2.2.2 Création de la base de donnée contenant des exemples

    python tools/exemple_db.py

## 2.3 Lancement de l'application

    export FLASK_APP=hello
    export FLASK_ENV=development
    flask run

# 3 Tests

## 3.1 Lacement de l'analyse statique

    pylint --load-plugins pylint_flask $(find . -name "*.py" | xargs)

## 3.2 Lancement des tests
    pytest
