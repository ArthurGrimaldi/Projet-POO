from classes.utilisateur import Utilisateur_Existant

import uuid

import numpy as np 
import pandas as pd 

class RecommenderSystem():
    def __init__(self):
        """
        ### Objectif
        Créer une nouvelle instance de la classe RecommenderSystem.
        """

        self._id = uuid.uuid4()

    @property
    def id(self):
        """
        ### Objectif
        Retourne l'identifiant du système de recommandation.
        """

        return self._id

    def favoriteGenres(self, user: Utilisateur_Existant):
        """
        ### Objectif
        Retourne les genres de livres préférés par l'utilisateur.
        ### Paramètres
        - user (Utilisateur_Existant): L'utilisateur pour lequel on veut les genres de livres préférés.
        ### Retourne
        - genres_list (list): La liste des genres de livres préférés par l'utilisateur.
        """
        
        genres_list = []

        user_book_index = [int(x) for x in user._liste_livres]
        books = pd.read_csv('data/books.csv', sep=',')

        for book in books.itertuples():
            if book.ID in user_book_index:
                genres_list.append(book.Genre)
            
        return genres_list
    
    def getBooksByGenres(self, user: Utilisateur_Existant):
        """
        ### Objectif
        Retourne les livres de la base de données qui correspondent aux genres de livres préférés par l'utilisateur.
        ### Paramètres
        - user (Utilisateur_Existant): L'utilisateur pour lequel on veut les livres qui correspondent aux genres de livres préférés.
        ### Retourne
        - books (pandas.DataFrame): Les livres qui correspondent aux genres de livres préférés par l'utilisateur.
        """

        books = pd.read_csv('data/books.csv', sep=',')

        return books[books['Genre'].isin(self.favoriteGenres(user))].reset_index(drop=True)
    
    def meanRating(self, user: Utilisateur_Existant):
        """
        ### Objectif
        Calcule la moyenne des notes attribuées aux livres qui correspondent aux genres de livres préférés par l'utilisateur.
        ### Paramètres
        - user (Utilisateur_Existant): L'utilisateur pour lequel on veut calculer la moyenne des notes attribuées aux livres qui correspondent aux genres de livres préférés.
        ### Retourne
        - books (pandas.DataFrame): Les livres qui correspondent aux genres de livres préférés par l'utilisateur avec la moyenne des notes attribuées.
        """

        books = self.getBooksByGenres(user)
        books['Mean_Rating'] = books['Rating'].apply(lambda x: np.mean([float(y) for y in x.split(',')]) if str(x) != 'nan' else np.nan)
        
        return books
        
    def calculateTopK(self, user: Utilisateur_Existant, k: int):
        """
        ### Objectif
        Récupère le nombre k de livres qui correspondent aux genres de livres préférés par l'utilisateur avec leur moyenne de notes attribuées.
        ### Paramètres
        - user (Utilisateur_Existant): L'utilisateur pour lequel on veut récupérer les livres qui correspondent aux genres de livres préférés.
        - k (int): Le nombre de livres à récupérer.
        ### Retourne
        - books (pandas.DataFrame): Les k livres qui correspondent aux genres de livres préférés par l'utilisateur avec leur moyenne de notes attribuées.
        """

        return self.meanRating(user).sort_values(by='Mean_Rating', ascending=False).head(k).reset_index(drop=True)

    def __str__(self):
        """
        ### Objectif
        Retourne une chaîne de caractères représentant l'instance de la classe RecommenderSystem.
        """
        
        return f"RecommenderSystem(id={self.id})"