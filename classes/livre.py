import uuid
from datetime import datetime

class Livre:
    def __init__(self, titre: str, auteurs, edition: str, genre):
        self._id = uuid.uuid4()
        self._titre = titre
        self._auteurs = auteurs
        self._edition = edition
        self._genre = genre
        self._note = []
        self._date_enregistrement = datetime.now().strftime('%d/%m/%Y:%H:%M:%S')
        
        self._historique = []
        
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
    def auteurs(self):
        return self._auteurs
    
    @auteurs.setter
    def auteurs(self, new_auteurs):
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
