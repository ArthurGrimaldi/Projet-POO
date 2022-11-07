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
        self._horaires = {'ouverture_heure': ouverture_heure,
                          'fermeture_heure': fermeture_heure}

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, new_nom: str):
        self._nom = new_nom
        return

    @property
    def lieu(self):
        return self._lieu

    @lieu.setter
    def lieu(self, new_lieu: str):
        self._lieu = new_lieu
        return

    @property
    def horaires(self):
        return self._horaires

    @horaires.setter
    def horaires(self, new_horaires):
        self._horaires = new_horaires
        return
