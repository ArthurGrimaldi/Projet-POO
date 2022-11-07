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

    @property
    def heure(self):
        return self._heure
    
    @property
    def occupe(self):
        return self._occupe