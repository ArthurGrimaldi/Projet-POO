import uuid
import typing
import pandas as pd 
import json
import numpy as np 

from classes.utilisateur import Utilisateur_Existant

class RecommenderSystem():
    def __init__(self):
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    def favoriteGenres(self, user: Utilisateur_Existant):
        genres_list = []
        user_book_index = [int(x) for x in user._liste_livres]

        with open('books.json') as file:
            books_json = json.load(file)

            for book in books_json:
                if book['ID'] in user_book_index:
                    genres_list.append(book['Genre'])
            
        return genres_list
    
    def getBooksByGenres(self, user: Utilisateur_Existant):
        books = pd.read_json('books.json')

        return books[books['Genre'].isin(self.favoriteGenres(user))].reset_index(drop=True)
    
    def meanRating(self, user: Utilisateur_Existant):
        books = self.getBooksByGenres(user)
        books['Mean_Rating'] = books['Rating'].apply(lambda x: np.mean(x) if len(x) > 0 else 'No rating yet')

        return books
        
    def calculateTopK(self, user: Utilisateur_Existant, k: int):

        return self.meanRating(user).sort_values(by='Mean_Rating', ascending=False).head(k).reset_index(drop=True)

