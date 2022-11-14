import uuid
from datetime import date, datetime


class Utilisateur:

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Purpose
        Créer un Utilisateur commun (différent d'un Admin).\n
        Nécessite d'input un nom et une date de naissance (format date).\n
        ID génère automatiquement des ID uniques en fonction de la datetime actuelle (import uuid)

        ### Args
            nom (str): Nom de l'utilisateur
            date_naissance (date): Date de naissance de l'utilisateur au format date
        """
        self._id = uuid.uuid1()
        self._nom = nom
        self._date_naissance = date_naissance
        self._statut = "Standard"
        self._date_enregistrement = datetime.now()
        
        self._emprunt_jour = False

        self._liste_livres = {
            "ID" : Livre._id,
            "date emprunt" : datetime
        }

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, new_nom):
        self._nom = new_nom
        return self._nom

    @property
    def date_naissance(self):
        return self._date_naissance
    
    @date_naissance.setter
    def date_naissance(self, new_date_naissance):
        self._date_naissance = new_date_naissance
        return self._date_naissance

    @property
    def statut(self):
        return self._statut
    
    @statut.setter
    def statut(self, new_statut):
        self._statut = new_statut
        return self._statut

    @property
    def date_enregistrement(self):
        return self._date_enregistrement


class Admin(Utilisateur):

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Purpose
        Hérite de toutes les propriétés d'Utilisateur.\n
        Change le statut de Standard à Admin.

        Args:
            nom (str): Nom du nouvel administrateur.
            date_naissance (date): Date de naissance du nouvel administrateur.
        """
        super().__init__(nom, date_naissance)
        self.statut = "Admin"
