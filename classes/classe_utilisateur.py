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


class Utilisateur_Admin(Utilisateur):

    def __init__(self, nom: str, date_naissance: date):
        super().__init__(nom, date_naissance)
        self.statut = "Admin"
