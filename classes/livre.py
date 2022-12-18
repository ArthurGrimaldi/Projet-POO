from datetime import datetime
import pandas as pd 

class Livre:
    def __init__(self, titre: str, auteur: str, edition: str, genre: str, pages: int):
        """
        ### Objectif
        Créer un objet Livre.

        ### Paramètres
        - titre (str): Le titre du livre.
        - auteur (str): L'auteur du livre.
        - edition (str): L'édition du livre.
        - genre (str): Le genre du livre.
        - pages (int): Le nombre de pages du livre.
        """
        self._id = len(pd.read_csv('data/books.csv', sep=','))
        self._titre = titre
        self._auteurs = auteur
        self._edition = edition
        self._genre = genre
        self._pages = pages
        self._note = "2"
        self._date_enregistrement = datetime.now().strftime('%d/%m/%Y::%H:%M:%S')        
        self._statut = True



    @property
    def id(self):
        """
        ### Objectif
        Retourne l'identifiant du livre.
        """
        return self._id
    
    @property
    def titre(self):
        """
        ### Objectif
        Retourne l'identifiant du livre.
        """
        return self._titre
    
    @titre.setter
    def titre(self, new_titre):
        """
        ### Objectif
        Modifie le titre du livre.
        ### Paramètres
        - new_titre (str): Le nouveau titre du livre.
        ### Retourne 
        Le titre du livre.
        """
        self._titre = new_titre
        return self._titre
    
    @property
    def auteur(self):
        """
        ### Objectif
        Retourne l'auteur du livre.
        """
        return self._auteurs
    
    @auteur.setter
    def auteur(self, new_auteur):
        """
        ### Objectif
        Modifie l'auteur du livre.
        ### Paramètres
        - new_auteur(str): Le nouvel auteur du livre.
        ### Retourne 
        L'auteur du livre.
        """
        self._auteurs = new_auteur
        return self._auteurs
    
    @property
    def edition(self):
        """
        ### Objectif
        Retourne l'édition du livre.
        """
        return self._edition
    
    @edition.setter
    def edition(self, new_edition):
        """
        ### Objectif
        Modifie l'éditeur du livre.
        ### Paramètres
        - new_edition (str): Le nouvel éditeur du livre.
        ### Retourne 
        L'éditeur du livre.
        """
        self._edition = new_edition
        return self._edition
    
    @property
    def genre(self):
        """
        ### Objectif
        Retourne le genre du livre.
        """
        return self._genre
    
    @genre.setter
    def genre(self, new_genre):
        """
        ### Objectif
        Modifie le genre du livre.
        ### Paramètres
        - new_genre (str): Le nouveau genre du livre.
        ### Retourne 
        Le genre du livre.
        """
        self._genre = new_genre
        return self._genre

    @property
    def note(self):
        """
        ### Objectif
        Retourne les notes du livre.
        """
        return self._note

    @property
    def date_enregistrement(self):
        """
        ### Objectif
        Retourne la date d'enregistrement du livre.
        """
        return self._date_enregistrement

    def __str__(self):
        """
        ### Objectif
        Retourne une représentation textuelle du livre.
        """
        
        return f"ID: {self._id} \n Titre: {self._titre} \n Auteur(s): {self._auteurs} \n Edition: {self._edition} \n Genre: {self._genre} \n Pages: {self._pages} \n Note: {self._note} \n Date d'enregistrement: {self._date_enregistrement} \n Statut: {self._statut}"