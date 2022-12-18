from classes.livre import Livre

from datetime import date, datetime
import uuid
import yaml

import pandas as pd

class Utilisateur_Nouveau:

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Objectif
        Créer un objet nouvel utilisateur.
        ### Paramètres
        - nom (str): Le nom de l'utilisateur.
        - date_naissance (date): La date de naissance de l'utilisateur.
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
        """
        ### Objectif
        Retourne l'identifiant de l'utilisateur.
        """

        return self._id

    @property
    def nom(self):
        """
        ### Objectif
        Retourne le nom de l'utilisateur.
        """

        return self._nom
    
    @nom.setter
    def nom(self, new_nom):
        """
        ### Objectif
        Modifie le nom de l'utilisateur.
        ### Paramètres
        - new_nom (str): Le nouveau nom de l'utilisateur.
        ### Retourne
        Le nom de l'utilisateur.
        """

        self._nom = new_nom

        return self._nom

    @property
    def date_naissance(self):
        """
        ### Objectif
        Retourne la date de naissance de l'utilisateur.
        """

        return self._date_naissance
    
    @date_naissance.setter
    def date_naissance(self, new_date_naissance):
        """
        ### Objectif
        Modifie la date de naissance de l'utilisateur.
        ### Paramètres
        - new_date_naissance (date): La nouvelle date de naissance de l'utilisateur.
        ### Retourne
        La date de naissance de l'utilisateur.
        """

        self._date_naissance = new_date_naissance

        return self._date_naissance

    @property
    def role(self):
        """
        ### Objectif
        Retourne l'identifiant de l'utilisateur.
        """

        return self._role
    
    @role.setter
    def role(self, new_role):
        """
        ### Objectif
        Modifie le rôle de l'utilisateur.
        ### Paramètres
        - new_role (str): Le nouveau rôle de l'utilisateur.
        ### Retourne
        Le rôle de l'utilisateur.
        """

        self._role = new_role

        return self._role

    @property
    def date_enregistrement(self):
        """
        ### Objectif
        Retourne la date d'enregistrement de l'utilisateur.
        """

        return self._date_enregistrement
    
    def _modifyListBooksInUsersCSV(self):
        """
        ### Objectif
        Modifie la liste des livres de l'utilisateur dans le fichier data/users.csv.
        """

        users = pd.read_csv('data/users.csv', sep=',')
        users.loc[users[users['id'] == self._id].index, 'liste_livres'] = self._liste_livre
        users.to_csv('data/users.csv', index=False)

        return 

    def rechercher(self, valeur_recherche: str, type_recherche: str):
        """
        ### Objectif
        Recherche un livre dans la base de données.
        ### Paramètres
        - valeur_recherche (str): La valeur à rechercher.
        - type_recherche (str): Le type de recherche (Titre, Auteur, Genre, Édition).
        ### Retourne
        Un DataFrame contenant les livres trouvés.
        """

        if type_recherche == "Titre":
            type_recherche = 'Title'
        elif type_recherche == "Auteur":
            type_recherche = 'Author'
        elif type_recherche == "Genre":
            type_recherche = 'Genre'
        elif type_recherche == "Éditeur":
            type_recherche = 'Publisher'


        livres = pd.read_csv("data/books.csv", sep=",")
        liste = pd.DataFrame(columns=livres.columns)
        for livre in livres.iterrows():
            if valeur_recherche.lower() in livre[1][type_recherche].lower():
                liste = pd.concat([liste, livre[1].to_frame().T], ignore_index=True)
 
        return liste
    
    def rechercherDansListeUtilisateur(self, valeur_recherche: str, type_recherche: str):
        """
        ### Objectif
        Recherche un livre dans la liste des livres de l'utilisateur.
        ### Paramètres
        - valeur_recherche (str): La valeur à rechercher.
        - type_recherche (str): Le type de recherche (Titre, Auteur, Genre, Édition).
        ### Retourne
        Un DataFrame contenant les livres trouvés.
        """
        
        if type_recherche == "Titre":
            type_recherche = 'Title'
        elif type_recherche == "Auteur":
            type_recherche = 'Author'
        elif type_recherche == "Genre":
            type_recherche = 'Genre'
        elif type_recherche == "Éditeur":
            type_recherche = 'Publisher'


        livres_bdd = pd.read_csv("data/books.csv", sep=",")
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
        """
        ### Objectif
        Emprunte un livre.
        ### Paramètres
        - livre_id (int): L'identifiant du livre à emprunter.
        """
        # modifie le statut du livre emprunté dans le csv books
        books = pd.read_csv('data/books.csv', sep=',')
        books.loc[books['ID'] == livre_id, 'Available'] = False
        books.loc[books['ID'] == livre_id, 'Loan_Date'] = datetime.now().strftime('%Y-%m-%d')
        books.loc[books['ID'] == livre_id, 'Loan_User_ID'] = self._id
        books.to_csv('data/books.csv', index=False)
        
        # ajoute l'id du livre à la liste des livres empruntés
        self._liste_livres.append(str(livre_id))

        # modifie la liste des livres empruntés dans le csv users
        users = pd.read_csv('data/users.csv', sep=',')
        row = users.loc[users['id'] == self._id]
        row['liste_livres'].values[0] = ','.join(self._liste_livres)
        users.loc[users['id'] == self._id] = row
        users.to_csv('data/users.csv', index=False)
        
        return 
        # Ajouter une variable contenant la date d'emprunt

    def _ajoutNoteLivre(self, livre_id: int, note: int):
        """
        ### Objectif
        Ajoute une note à un livre.
        ### Paramètres
        - livre_id (int): L'identifiant du livre.
        - note (int): La note à ajouter.
        """

        books = pd.read_csv('data/books.csv', sep=',')
        book_row = books.loc[books['ID'] == livre_id]

        if str(book_row['Rating'].values[0]) == 'nan':
            books.loc[books['ID'] == livre_id, 'Rating'] = str(note)
            books.to_csv('data/books.csv', index=False)

            return

        else:
            book_note_previous = str(book_row['Rating'].values[0]).split(',')
            book_note_previous.append(str(note))
            book_row['Rating'] = ','.join(book_note_previous)
            books.loc[books['ID'] == livre_id] = book_row
            books.to_csv('data/books.csv', index=False)

        return

    def retourner(self, livre_id: int, note: int):
        """
        ### Objectif
        Rendre un livre.
        ### Paramètres
        - livre_id (int): L'identifiant du livre à rendre.
        - note (int): La note à ajouter au livre.
        """

        books = pd.read_csv('data/books.csv', sep=',')
        books.loc[books['ID'] == livre_id, 'Available'] = True
        books.to_csv('data/books.csv', index=False)

        self._liste_livres.remove(str(livre_id))

        users = pd.read_csv('data/users.csv', sep=',')
        row = users.loc[users['id'] == self._id]
        row['liste_livres'].values[0] = ','.join(self._liste_livres)
        users.loc[users['id'] == self._id] = row
        users.to_csv('data/users.csv', index=False)
        
        self._ajoutNoteLivre(livre_id, note)

        return 

    def _addUserToCSV(self):
            """
            ### Objectif
            Ajoute le nouvel utilisateur à la base de données des utilisateurs.
            """

            users = pd.read_csv('data/users.csv', sep=',')
            users = users.append({
                'id': self._id, 
                'nom': self._nom, 
                'date_naissance': self._date_naissance, 
                'role': self._role, 
                'date_enregistrement': self._date_enregistrement, 
                'emprunt_jour': self._emprunt_jour, 
                'liste_livres': self._liste_livres
            }, ignore_index=True)
            users.to_csv('data/users.csv', index=False)

            return

    def inscription(self, username, mail, pwd):
        """
        ### Objectif
        Inscrire un nouvel utilisateur à la base de données YAML.
        ### Paramètres
        - username (str): Le nom d'utilisateur.
        - mail (str): L'adresse mail.
        - pwd (str): Le mot de passe.
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

        # update the data/users.csv database with the new user
        self._addUserToCSV()

        return 






class Utilisateur_Existant(Utilisateur_Nouveau):
    
    def __init__(self, id: str, nom: str, date_naissance: date, role: str, date_enregistrement: date, liste_livres: list):
        """
        ### Objectif
        Créer une instance d'un utilisateur déjà enregisré dans la base de données.
        ### Paramètres
        - id (str): L'identifiant de l'utilisateur.
        - nom (str): Le nom de l'utilisateur.
        - date_naissance (date): La date de naissance de l'utilisateur.
        - role (str): Le rôle de l'utilisateur.
        - date_enregistrement (date): La date d'enregistrement de l'utilisateur.
        - liste_livres (list): La liste des livres empruntés par l'utilisateur.
        """

        self._id = id
        self._nom = nom
        self._date_naissance = date_naissance
        self._role = role
        self._date_enregistrement = date_enregistrement
        self._liste_livres = liste_livres






class Admin(Utilisateur_Nouveau):

    def __init__(self, nom: str, date_naissance: date):
        """
        ### Objectif
        Créer une instance d'un administrateur.
        ### Paramètres
        - nom (str): Le nom de l'administrateur.
        - date_naissance (date): La date de naissance de l'administrateur.
        """

        super().__init__(nom, date_naissance)
        self._role = "Admin"

        self._ajouterAdminCSV()

    def _ajouterAdminCSV(self):
        """
        ### Objectif
        Ajoute le nouvel administrateur à la base de données des utilisateurs.
        """

        users = pd.read_csv('data/users.csv', sep=',')
        users = users.append({
            'id': self._id,
            'nom': self._nom,
            'date_naissance': self._date_naissance,
            'role': self._role,
            'date_enregistrement': self._date_enregistrement,
        }, ignore_index=True)
        users.to_csv('data/users.csv', index=False)

        return                
        
    def ajouterLivre(self, titre: str, auteur: str, edition: str, genre: str, pages: int):
        """
        ### Objectif
        Ajoute un nouveau livre à la base de données des livres.

        ### Paramètres
            titre (str): titre du livre
            auteur (str): autour du livre
            edition (str): edition du livre
            genre (str): genre du livre
            pages (int): nombre de pages du livre
        """

        livre_ajout = Livre(titre, auteur, edition, genre, pages)
        
        livres = pd.read_csv('data/books.csv', sep=',')
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
        }])], ignore_index=True).to_csv('data/books.csv', index=False)

        return 
     
    def retirerLivre(self, livre_id: int):
        """
        ### Objectif
        Retire un livre de la base de données des livres.

        ### Paramètres
            livre_id (int): l'ID du livre
        """

        books = pd.read_csv('data/books.csv', sep=',')
        books = books[books['ID'] != livre_id]
        books.to_csv('data/books.csv', index=False)

        return 

    def notifierUtilisateurTempsEmprunt(self, user: Utilisateur_Existant, livre_id: int):
        """
        ### Objectif
        Notifie l'utilisateur qu'il a dépassé le temps d'emprunt d'un livre.
        ### Paramètres
        - user (Utilisateur_Existant): L'utilisateur à notifier.
        - titre (str): Le titre du livre dont le temps d'emprunt est dépassé.
        ### Retourne
        - (str): Le temps d'emprunt.
        """
        livre_id = 5
        books = pd.read_csv('data/books.csv', sep=',')
        book = books[books['ID'] == livre_id]
        loan_date = book['Loan_Date'].values[0]

        now = datetime.now().strftime('%Y-%m-%d')
        timedelta = datetime.strptime(now, '%Y-%m-%d') - datetime.strptime(loan_date, '%Y-%m-%d')

        # if the difference is greater than 30 days, notify the user
        if timedelta.days > 30:
            return "Vous avez dépassé le temps d'emprunt du livre " + book['Title'].values[0] + "."
            
    
    def rechercher(self, valeur_recherche: str, type_recherche: str):
        """
        ### Objectif
        Recherche un livre dans la base de données des livres.
        ### Paramètres
        - valeur_recherche (str): La valeur à rechercher.
        - type_recherche (str): Le type de recherche.
        ### Retourne
        - (pd.DataFrame): La liste des livres correspondant à la recherche.
        """
        if type_recherche == "Titre":
            type_recherche = 'Title'
        elif type_recherche == "Auteur":
            type_recherche = 'Author'
        elif type_recherche == "Genre":
            type_recherche = 'Genre'
        elif type_recherche == "Éditeur":
            type_recherche = 'Publisher'


        livres = pd.read_csv("data/books.csv", sep=",")
        liste = pd.DataFrame(columns=livres.columns)
        for livre in livres.iterrows():
            if valeur_recherche.lower() in livre[1][type_recherche].lower():
                liste = pd.concat([liste, livre[1].to_frame().T], ignore_index=True)
 
        return liste





class Admin_Existant(Admin):
    
    def __init__(self, id: str, nom: str, date_naissance: date, role: str, date_enregistrement: date):
        """
        ### Objectif
        Créer une instance d'un administrateur existant.
        ### Paramètres
        - id (str): L'ID de l'administrateur.
        - nom (str): Le nom de l'administrateur.
        - date_naissance (date): La date de naissance de l'administrateur.
        - role (str): Le rôle de l'administrateur.
        - date_enregistrement (date): La date d'enregistrement de l'administrateur.
        """
        
        self._id = id
        self._nom = nom
        self._date_naissance = date_naissance
        self._role = role
        self._date_enregistrement = date_enregistrement
 
