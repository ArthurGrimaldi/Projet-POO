import uuid


class Reservation:
    """
    ### Purpose

    """

    def __init__(self, jour: str, heure: str, occupe: bool):
        self._id = uuid.uuid4()
        self._jour = jour
        self._heure = heure
        self._occupe = occupe

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
    def occupe(self):
        return self._occupe

    @occupe.setter
    def occupe(self, new_occupe):
        self._occupe = new_occupe
