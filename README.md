# 1. Premier pas d'utilisation de flask

Ce projet a été construit avec l'aide des tutoriels suivant : 
- [Comment créer une application web en utilisant Flask en Python 3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-fr)
- [Comment ajouter une authentification à votre application avec Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-fr)

# 2. Utilisation

## 2.1 Installation des prérequis
    pip install -r requirements.txt

## 2.2 Création de la base de donnée

    python init_db.py

## 2.3 Lancement de l'application

    export FLASK_APP=hello
    export FLASK_ENV=development
    flask run

