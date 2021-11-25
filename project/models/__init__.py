"""Model de donnée pour le stockage des articles"""
import markdown
from sqlalchemy.sql import func

from project import db


class Article(db.Model):
    """
    Classe de donnée pour le stockage d'un article
    """
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(256), index=True, unique=False)
    contenu = db.Column(db.String(), index=True, unique=False)
    date_creation = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_miseajour = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        """
        Représentation textuel d'un article
        :return:  la représentation textuel d'un article
        """
        return f'<Article({self.id}): {self.titre}>'

    def markdown_content(self):
        return markdown.markdown(self.content)
