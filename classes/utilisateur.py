import uuid
from datetime import date, datetime
from livre import Livre
import yaml


class Utilisateur:

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Purpose
        Créer un Utilisateur commun (différent d'un Admin).\n
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
        
        self._emprunt_jour = False

        self._liste_livres = []

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, new_nom):
        self._nom = new_nom
        return self._nom

    @property
    def date_naissance(self):
        return self._date_naissance
    
    @date_naissance.setter
    def date_naissance(self, new_date_naissance):
        self._date_naissance = new_date_naissance
        return self._date_naissance

    @property
    def statut(self):
        return self._statut
    
    @statut.setter
    def statut(self, new_statut):
        self._statut = new_statut
        return self._statut

    @property
    def date_enregistrement(self):
        return self._date_enregistrement

    def retourner(self):
        """
        ### Returns:
             _type_: _description_
            
         ### Final :
         Si toutes les conditions d'emprunt sont remplies, la méthode va :\n
             - Ajouter l'ID du livre à la liste de livres empruntés par le User,
             - Changer self.emprunt_jour à True pour User
             - Changer self._statut à False pour Livre (False = emprunté)
        """
        if self._emprunt_jour == True:
            return "Vous ne pouvez plus emprunter de livres aujourd'hui. Revenez Demain !"
        if len(self._liste_livres) == 5 :
            return "Vous avez déjà emprunté 5 livres. Retournez en un afin de pouvoir en emprunter un autre !"
        livre = {
            "Titre" : str(input("Insérer le titre du livre :")),
            "Auteur" : str(input("Insérer l'auteur du livre :"))
        }
    # Ajouter rechercher() pour utiliser livre et resortir l'ID du livre
    # Ajouter une variable contenant la date d'emprunt
    

    def emprunter(self, livre = Livre):
        """
        Args:
            livre (Livre, optional): Objet Livre. Defaults to Livre.

        Returns:
            _type_: _description_
            
        ### Final :
        Si toutes les conditions de retour sont remplies, la méthode va :
            - Ajouter la note à la liste de notes du livre,
            - Retirer l'ID du livre de la liste d'emprunts de l'User,
            - Changer self._statut du Livre à True,
            - Ajouter à la liste _historique du livre l'ID de l'User, la date d'emprunt et la date de retour du livre.
        """
        if livre._id not in self._liste_livres:
            raise ValueError("Ce livre ne fait pas partie des livres empruntés.")
        while True:
            try:
                note = int(input("Entrer une note pour le livre :"))
                if note < 0 or note > 5:
                    raise ValueError
                break
            except ValueError:
                return "La note doit être un chiffre rond."
        
        livre._note.append(note)
        self._liste_livres = self._liste_livres.remove(livre._id)
        livre.statut = True
        livre._historique = livre._historique.append({
            "user": self._id,
            "date emprunt": self._liste_livres("date emprunt"),
            "date retour": datetime.now()
        })

    def inscription(self, username, mail, pwd):
        with open("config.yaml") as file:
            config = yaml.safe_load(file)

            config['credentials']['usernames'].update({
                username: {
                    "email": mail,
                    "name": username,
                    "password" : pwd
                }
            })

        with open("config.yaml", 'w') as file:
            yaml.dump(config, file)

        return 


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
