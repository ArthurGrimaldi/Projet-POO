import uuid

class Bibliotheque:
    """
    ### Purpose
    Créer une bibliothèque
    """

    def __init__(self, nom: str, lieu: str, ouverture_heure, fermeture_heure: str):
        self._id = uuid.uuid4()
        self._nom = nom
        self._lieu = lieu 
        self._horaires = {'ouverture_heure': ouverture_heure,'fermeture_heure': fermeture_heure}
    
    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def lieu(self):
        return self._lieu

    @property
    def horaires(self):
        return self._horaires