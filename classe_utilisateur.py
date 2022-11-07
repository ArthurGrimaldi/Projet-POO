import uuid
from datetime import date, datetime

class Utilisateur :
    """
    ### Purpose
    Créer un Utilisateur commun (différent d'un Utilisateur_Admin).\n
    Nécessite d'input un nom et une date de naissance (format date).\n
    ID génère automatiquement des ID uniques en fonction de la datetime actuelle (import uuid)
    """
    
    def __init__(self, nom : str, date_naissance : date) -> None:
        self.id = uuid.uuid1()
        self.nom = nom
        self.date_naissance = date_naissance
        self.statut = "Utilisateur Commun"
        self.date_enregistrement = datetime.now()