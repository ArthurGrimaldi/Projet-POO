import uuid
from datetime import date, datetime
import yaml
import pandas as pd
import os
import streamlit_authenticator as stauth
from classes.livre import Livre
import numpy as np
import csv 



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
        self._role = "Utilisateur"
        self._date_enregistrement = datetime.now()
        
        self._emprunt_jour = True

        self._liste_livres = "0"

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
    def role(self):
        return self._role
    
    @role.setter
    def role(self, new_role):
        self._role = new_role
        return self._role

    @property
    def date_enregistrement(self):
        return self._date_enregistrement
    
    def _modifyListBooksInUsersCSV(self):
        users = pd.read_csv('users.csv', sep=',')
        users.loc[users[users['id'] == self._id].index, 'liste_livres'] = self._liste_livre
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
    
    def rechercherDansListeUtilisateur(self, valeur_recherche: str, type_recherche: str):
        
        if type_recherche == "Titre":
            type_recherche = 'Title'
        elif type_recherche == "Auteur":
            type_recherche = 'Author'
        elif type_recherche == "Genre":
            type_recherche = 'Genre'
        elif type_recherche == "Éditeur":
            type_recherche = 'Publisher'


        livres_bdd = pd.read_csv("books.csv", sep=",")
        livre_user_bdd = pd.DataFrame(columns=livres_bdd.columns)
        livres_utilisateur = self._liste_livres
        for livre_user in livres_utilisateur:
            livre_user_bdd = pd.concat([livre_user_bdd, livres_bdd.loc[livres_bdd['ID'] == int(livre_user)]], ignore_index=True)
        
        liste = pd.DataFrame(columns=livres_bdd.columns)
        for livre in livre_user_bdd.iterrows():
            if valeur_recherche.lower() in livre[1][type_recherche].lower():
                liste = pd.concat([liste, livre[1].to_frame().T], ignore_index=True)
 
        return liste
            
    def emprunter(self, livre_id: int):
        # modifie le statut du livre emprunté dans le csv books
        books = pd.read_csv('books.csv', sep=',')
        books.loc[books['ID'] == livre_id, 'Available'] = False
        books.to_csv('books.csv', index=False)
        
        # ajoute l'id du livre à la liste des livres empruntés
        self._liste_livres.append(str(livre_id))

        # modifie la liste des livres empruntés dans le csv users
        users = pd.read_csv('users.csv', sep=',')
        row = users.loc[users['id'] == self._id]
        row['liste_livres'].values[0] = ','.join(self._liste_livres)
        users.loc[users['id'] == self._id] = row
        users.to_csv('users.csv', index=False)
        
        return 
        # Ajouter une variable contenant la date d'emprunt

    def _ajoutNoteLivre(self, livre_id: int, note: int):
    
        books = pd.read_csv('books.csv', sep=',')
        book_row = books.loc[books['ID'] == livre_id]

        if str(book_row['Rating'].values[0]) == 'nan':
            books.loc[books['ID'] == livre_id, 'Rating'] = str(note)
            books.to_csv('books.csv', index=False)
            return
        else:
            book_note_previous = str(book_row['Rating'].values[0]).split(',')
            book_note_previous.append(str(note))
            book_row['Rating'] = ','.join(book_note_previous)
            books.loc[books['ID'] == livre_id] = book_row
            books.to_csv('books.csv', index=False)
        return

    def retourner(self, livre_id: int, note: int):
        
        books = pd.read_csv('books.csv', sep=',')
        books.loc[books['ID'] == livre_id, 'Available'] = True
        books.to_csv('books.csv', index=False)

        self._liste_livres.remove(str(livre_id))

        users = pd.read_csv('users.csv', sep=',')
        row = users.loc[users['id'] == self._id]
        row['liste_livres'].values[0] = ','.join(self._liste_livres)
        users.loc[users['id'] == self._id] = row
        users.to_csv('users.csv', index=False)
        
        self._ajoutNoteLivre(livre_id, note)

        return 
        
        # livre._historique = livre._historique.append({
        #     "user": self._id,
        #     "date emprunt": self._liste_livres("date emprunt"),
        #     "date retour": datetime.now()
        # })

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
                'role': self._role, 
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
    
    def __init__(self, id: str, nom: str, date_naissance: date, role: str, date_enregistrement: date, liste_livres: list):
        self._id = id
        self._nom = nom
        self._date_naissance = date_naissance
        self._role = role
        self._date_enregistrement = date_enregistrement
        # self._emprunt_jour = emprunt_jour
        self._liste_livres = liste_livres

class Admin(Utilisateur_Nouveau):

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Purpose
        Hérite de toutes les propriétés d'Utilisateur.\n
        Change le rôle de Standard à Admin.
        Args:
            nom (str): Nom du nouvel administrateur.
            date_naissance (date): Date de naissance du nouvel administrateur.
        """
        super().__init__(nom, date_naissance)
        self._role = "Admin"
        
    # def ajouter_livres_a_librairie()
    def ajouterLivre(self, titre: str, auteur: str, edition: str, genre: str, pages: int):
        info = {
            "titre": 'Sapiens',
            "auteur": 'Yuval Noah Harari',
            "edition": 'Pocket',
            "genre": 'Histoire',
            "pages": 464
        }
        livre_ajout = Livre(
            info['titre'],
            info['auteur'],
            info['edition'],
            info['genre'],
            info['pages']
        )
        
        
        livres = pd.read_csv('books.csv', sep=',')
        # add the new book to the database
        pd.concat([livres, pd.DataFrame([{
            'ID': livre_ajout._id,
            'Title': livre_ajout._titre,
            'Author': livre_ajout._auteurs,
            'Publisher': livre_ajout._edition,
            'Genre': livre_ajout._genre,
            'Height': livre_ajout._pages,
            'Available': livre_ajout._statut,
            'Rating': livre_ajout._note,
        }])], ignore_index=True).to_csv('books.csv', index=False)

        
    # def retirer_livres_a_librairie()
        
    def notifier_utilisateur_temps_emprunt(self, user : Utilisateur_Existant, titre : str):
        livre = user._liste_livres[user._liste_livres["titre" == titre]]
        date_emprunt_livre = livre["date"]
        date = datetime.now()
        temps_emprunt = date - date_emprunt_livre
        
        return temps_emprunt

# livre_test = Livre("Sapiens", "Yuval Noah Harari", "Pocket", "Histoire", 464)