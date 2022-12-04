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

        if liste.empty:
            print("Aucun livre ne correspond à votre recherche.")
        else:     
            return liste
            
    def emprunter(self, livre : str, type_recherche : str):
        """
        ### Returns:
             _type_: _description_
            
         ### Final :
         Si toutes les conditions d'emprunt sont remplies, la méthode va :
             - Ajouter l'ID du livre à la liste de livres empruntés par le User,
             - Changer self.emprunt_jour à True pour User
             - Changer self._statut à False pour Livre (False = emprunté)
        """
        if self._emprunt_jour == True:
            return "Vous ne pouvez plus emprunter de livres aujourd'hui. Revenez Demain !"

        if len(self._liste_livres) >= 5 :
            return "Vous avez déjà emprunté 5 livres. Retournez en un afin de pouvoir en emprunter un autre !"

        recherche = self.rechercher(valeur_recherche= livre, type_recherche= type_recherche)
        
        if recherche == 0:
            return "Le livre recherché n'est pas disponible dnas cette bibliothèque."
        elif max(recherche.index) > 1:
            print(f"Votre recherche retourne plusieurs livres :\n {self.rechercher(livre)}\n Veuillez préciser votre recherche.")
        else:
            livre1 = self.rechercher(livre)
            instan_livre = Livre(titre= livre1.Title)
            
    # Ajouter rechercher() pour utiliser livre et resortir l'ID du livre
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


class Utilisateur_Existant(Utilisateur_Nouveau):
    
    def __init__(self, id : str, nom : str, date_naissance : date, statut : str, date_enregistrement : date, emprunt_jour : bool, liste_livres : list):
        self._id = id
        self._nom = nom
        self._date_naissance = date_naissance
        self._statut = statut
        self._date_enregistrement = date_enregistrement
        self._emprunt_jour = emprunt_jour
        self._liste_livres = liste_livres