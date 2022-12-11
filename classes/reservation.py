import uuid


class Reservation:
    """
    ### Purpose

    """

    def __init__(self, jour: str, heure: str, disponible: bool):
        self._id = uuid.uuid4()
        self._jour = jour
        self._heure = heure
        self._occupe = disponible

        self._utilisateur = None

    @property
    def id(self):
        return self._id

    @property
    def jour(self):
        return self._jour

    @jour.setter
    def jour(self, new_jour):
        self._jour = new_jour
        return

    @property
    def heure(self):
        return self._heure

    @heure.setter
    def heure(self, new_heure):
        self._heure = new_heure

    @property
    def disponible(self):
        return self._occupe

    @disponible.setter
    def disponible(self, new_dispo):
        self._occupe = new_dispo

    
