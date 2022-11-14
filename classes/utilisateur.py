import uuid
from datetime import date, datetime


class Utilisateur:

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Purpose
        Créer un Utilisateur commun (différent d'un Utilisateur_Admin).\n
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
        
        self._emprunt = False

        self._liste_livres = []

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def statut(self):
        return self._statut

    @property
    def statut(self):
        return self._date_enregistrement
    
    def emprunter(self):
        if self.emprunt == True:
            return "Vous ne pouvez plus emprunter de livres aujourd'hui. Revenez Demain !"
        if len(self._liste_livres) == 5 :
            return "Vous avez déjà emprunté 5 livres. Retournez en un afin de pouvoir en emprunter un autre !"
        livre = {
            "Titre" : str(input("Insérer le titre du livre :")),
            "Auteur" : str(input("Insérer l'auteur du livre :"))
        }
    # Ajouter rechercher() pour utiliser livre et resortir l'ID du livre   



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
