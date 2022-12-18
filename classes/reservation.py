import uuid

class Reservation:

    def __init__(self, jour: str, heure: str, disponible: bool):
        """
        ### Objectif
        Initialise une réservation.
        ### Paramètres
        - jour (str): Le jour de la réservation.
        - heure (str): L'heure de la réservation.
        - disponible (bool): Si la réservation est disponible.
        """

        self._id = uuid.uuid4()
        self._jour = jour
        self._heure = heure
        self._occupe = disponible
        self._utilisateur = None

    @property
    def id(self):
        """
        ### Objectif
        Retourne l'identifiant de la réservation.
        """

        return self._id

    @property
    def jour(self):
        """
        ### Objectif
        Retourne le jour de la réservation.
        """

        return self._jour

    @jour.setter
    def jour(self, new_jour):
        """
        ### Objectif
        Modifie le jour de la réservation.
        ### Paramètres
        - new_jour (str): Le nouveau jour de la réservation.
        """

        self._jour = new_jour

        return

    @property
    def heure(self):
        """
        ### Objectif
        Retourne l'heure de la réservation.
        """

        return self._heure

    @heure.setter
    def heure(self, new_heure):
        """
        ### Objectif
        Modifie l'heure de la réservation.
        ### Paramètres
        - new_heure (str): La nouvelle heure de la réservation.
        """

        self._heure = new_heure

        return 

    @property
    def disponible(self):
        """
        ### Objectif
        Retourne  si la réservation est disponible ou non.
        """

        return self._occupe

    @disponible.setter
    def disponible(self, new_dispo):
        """
        ### Objectif
        Modifie la disponibilité de la réservation.
        ### Paramètres
        - new_dispo (bool): La nouvelle disponibilité de la réservation.
        """

        self._occupe = new_dispo

        return 

    def __str__(self):
        """
        ### Objectif
        Retourne une chaîne de caractères représentant la réservation.
        """

        return f"Réservation du {self._jour} à {self._heure}."
    
