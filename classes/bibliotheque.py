import uuid

class Bibliotheque:

    def __init__(self, nom: str, lieu: str, ouverture_heure: str, fermeture_heure: str):
        """
        ### Objectif
        Créer une nouvelle instance de la classe Bibliothèque.

        Args:
            nom (str): le nom de la bibliothèque
            lieu (str): le lieu de la bibliothèque
            ouverture_heure (str): l'heure d'ouverture de la bibliothèque
            fermeture_heure (str): l'heure de fermeture de la bibliothèque
        """

        self._id = uuid.uuid4()
        self._nom = nom
        self._lieu = lieu
        self._horaires = {
            'ouverture_heure': ouverture_heure,
            'fermeture_heure': fermeture_heure
        }

    @property
    def id(self):
        """
        ### Objectif
        Retourne l'identifiant de la bibliothèque.
        """

        return self._id

    @property
    def nom(self):
        """
        ### Objectif
        Retourne le nom de la bibliothèque.
        """
        
        return self._nom

    @nom.setter
    def nom(self, new_nom: str):
        """
        ### Objectif
        Modifie le nom de la bibliothèque.
        ### Paramètres
        - new_nom (str): Le nouveau nom de la bibliothèque.
        """

        self._nom = new_nom

        return

    @property
    def lieu(self):
        """
        ### Objectif
        Retourne le lieu de la bibliothèque.
        """
        
        return self._lieu

    @lieu.setter
    def lieu(self, new_lieu: str):
        """
        ### Objectif
        Modifie le lieu de la bibliothèque.
        ### Paramètres
        - new_lieu (str): Le nouveau lieu de la bibliothèque.
        """

        self._lieu = new_lieu
        
        return

    @property
    def horaires(self):
        """
        ### Objectif
        Retourne les horaires de la bibliothèque.
        """
    
        return self._horaires

    @horaires.setter
    def horaires(self, new_horaires):
        """
        ### Objectif
        Modifie les horaires de la bibliothèque.
        ### Paramètres
        - new_horaires (dict): Les nouveaux horaires de la bibliothèque.
        """

        self._horaires = new_horaires

        return
    
    def __str__(self):
        """
        ### Objectif
        Retourne une représentation textuelle de la bibliothèque.
        """

        return f"Nom: {self._nom} \n Lieu: {self._lieu} \n Horaires: {self._horaires} \n"