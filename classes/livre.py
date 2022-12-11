import uuid
from datetime import datetime
import typing
import pandas as pd 

class Livre:
    def __init__(self, titre: str, auteur: str, edition: str, genre: str, pages: int):
        self._id = len(pd.read_csv('books.csv', sep=','))
        self._titre = titre
        self._auteurs = auteur
        self._edition = edition
        self._genre = genre
        self._pages = pages
        self._note = "2"
        self._date_enregistrement = datetime.now().strftime('%d/%m/%Y::%H:%M:%S')
        
        # self._historique = []
        
        self._statut = True



    @property
    def id(self):
        return self._id
    
    @property
    def titre(self):
        return self._titre
    
    @titre.setter
    def titre(self, new_titre):
        self._titre = new_titre
        return self._titre
    
    @property
    def auteur(self):
        return self._auteurs
    
    @auteur.setter
    def auteur(self, new_auteurs):
        self._auteurs = new_auteurs
        return self._auteurs
    
    @property
    def edition(self):
        return self._edition
    
    @edition.setter
    def edition(self, new_edition):
        self._edition = new_edition
        return self._edition
    
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, new_genre):
        self._genre = new_genre
        return self._genre

    @property
    def note(self):
        return self._note

    @property
    def date_enregistrement(self):
        return self._date_enregistrement

