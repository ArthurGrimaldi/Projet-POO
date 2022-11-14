import uuid
from datetime import date, datetime
from livre import Livre


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
        
        self._emprunt_jour = False

        self._liste_livres = {
            "ID" : Livre._id,
            "date emprunt" : datetime
        }

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def statut(self):
        return self._statut

    @property
    def statut(self):
        return self._date_enregistrement
    
    def emprunter(self):
        """
        ### Purpose :
        Méthode définie afin d'emprunter un livre.\n
        Demande en input un titre et un auteur afin de ressortir l'ID du livre à emprunter.\n
        Check :
            - si le User a déjà fait un emprunt aujourd'hui 
            - s'il a déjà 5 livres empruntés (Si oui ValueError).\n

        ### Returns:
            _type_: _description_
            
        ### Final :
        Si toutes les conditions d'emprunt sont remplies, la méthode va :\n
            - Ajouter l'ID du livre à la liste de livres empruntés par le User,
            - Changer self.emprunt_jour à True pour User
            - Changer self._statut à False pour Livre (False = emprunté)
        """
        if self.emprunt == True:
            return "Vous ne pouvez plus emprunter de livres aujourd'hui. Revenez Demain !"
        if len(self._liste_livres) == 5 :
            return "Vous avez déjà emprunté 5 livres. Retournez en un afin de pouvoir en emprunter un autre !"
        livre = {
            "Titre" : str(input("Insérer le titre du livre :")),
            "Auteur" : str(input("Insérer l'auteur du livre :"))
        }
    # Ajouter rechercher() pour utiliser livre et resortir l'ID du livre
    # Ajouter une variable contenant la date d'emprunt
    
    def retourner(self, livre = Livre):
        """
        ### Purpose :
        Méthode définie afin de retourner un livre.\n
        Demande en entrée un livre présent dans la base.\n
        Check :
            - Si le livre a bien été emprunté par le User,
            - Si la note en input est un int,
            - Si la note en input est entre 0 et 5.

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
