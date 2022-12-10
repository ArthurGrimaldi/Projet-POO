import uuid
from datetime import date, datetime
import yaml
import pandas as pd
import os
import streamlit_authenticator as stauth
from classes.livre import Livre
import numpy as np



class Utilisateur_Nouveau:

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
    
    def _modifyListBooksInUsersCSV(self):
        users = pd.read_csv('users.csv', sep=',')
        users.loc[users[users['id'] == self._id].index, 'liste_livres'] = self._liste_livres
        users.to_csv('users.csv', index=False)
        return 

    def rechercher(self, valeur_recherche: str, type_recherche: str):
    
        if type_recherche == "Titre":
            type_recherche = 'Title'
        elif type_recherche == "Auteur":
            type_recherche = 'Author'
        elif type_recherche == "Genre":
            type_recherche = 'Genre'
        elif type_recherche == "Éditeur":
            type_recherche = 'Publisher'


        livres = pd.read_csv("books.csv", sep=",")
        liste = pd.DataFrame(columns=livres.columns)
        for livre in livres.iterrows():
            if valeur_recherche.lower() in livre[1][type_recherche].lower():
                liste = pd.concat([liste, livre[1].to_frame().T], ignore_index=True)
 
        return liste
            
    def emprunter(self, livre_id: str):
        print('ok 1')
        # modifie le statut du livre emprunté
        books = pd.read_csv('books.csv', sep=',')
        books.loc[books['ID'] == int(livre_id), 'Available'] = False
        print("ok 2")
        books.to_csv('books.csv', index=False)
        print("ok 3")
        self._liste_livres.append(int(livre_id))
        print("ok 4")
        users = pd.read_csv('users.csv', sep=',')
        print("ok 5")
        row = users.loc[users['id'] == self._id]
        print("ok 6")
        row['liste_livres'].values[0] = self._liste_livres
        print("ok 7")
        users.loc[users['id'] == self._id] = row
        print("ok 8")
        users.to_csv('users.csv', index=False)
        
        return 
        # Ajouter une variable contenant la date d'emprunt

    def retourner(self, livre):
        """
        Args:
            livre (Livre, optional): Objet Livre.
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

    def _addUserToCSV(self):
            """
            ### Objectif
            Ajoute le nouvel utilisateur à la base de données des utilisateurs.
            """
            users = pd.read_csv('users.csv', sep=',')
            users = users.append({
                'id': self._id, 
                'nom': self._nom, 
                'date_naissance': self._date_naissance, 
                'statut': self._statut, 
                'date_enregistrement': self._date_enregistrement, 
                'emprunt_jour': self._emprunt_jour, 
                'liste_livres': self._liste_livres
            }, ignore_index=True)
            users.to_csv('users.csv', index=False)
            return

    def inscription(self, username, mail, pwd):
        """
        Args:
            username (str): Nom d'utilisateur
            mail (str): Adresse mail
            pwd (str): Mot de passe
        
        Returns:
        ### Final :
        Configuration du fichier yaml pour l'authentification et mise à jour de la base
        de données des utilisateurs.
        """
        # update the yaml file with the new user
        with open("config.yaml") as file:
            config = yaml.safe_load(file)
            
            config['credentials']['usernames'].update({
                username: {
                    "email": mail,
                    "name": username,
                    "password" : pwd
                }
            })
            config['preauthorized']['emails'].append(mail)
        with open("config.yaml", 'w') as file:
            yaml.dump(config, file)

        # update the users.csv database with the new user
        self._addUserToCSV()

        return 
        
class Utilisateur_Existant(Utilisateur_Nouveau):
    
    def __init__(self, id : str, nom : str, date_naissance : date, statut : str, date_enregistrement : date, emprunt_jour : bool, liste_livres : list):
        self._id = id
        self._nom = nom
        self._date_naissance = date_naissance
        self._statut = statut
        self._date_enregistrement = date_enregistrement
        self._emprunt_jour = emprunt_jour
        self._liste_livres = liste_livres

class Admin(Utilisateur_Nouveau):

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
        
    def notifier_utilisateur_temps_emprunt(self, user : Utilisateur_Existant, titre : str):
        livre = user._liste_livres[titre]
        date = datetime.now()
        # Prendre la date du livre dans la liste
        # date - date d'emprunt
        # return le résultat

user = Utilisateur_Existant("65bcca28-73e7-11ed-83f1-3a010ad1daf8","fagzz","2022-12-04","Standard","2022-12-04 16:21:59.986453",False,"10,20".split(','))
user._liste_livres#.pop(2)
user.emprunter("30")
