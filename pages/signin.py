import streamlit as st 
import streamlit_authenticator as stauth
import yaml
import pandas as pd
from time import sleep
import numpy as np 

from classes.utilisateur import Utilisateur_Existant, Admin_Existant
from classes.reco_sys import RecommenderSystem

  

with open('config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Se connecter', 'main')
# authenticator.logout('Se déconnecter', 'main')

if authentication_status:
    # name = 'fagzz'
    users_csv = pd.read_csv('users.csv', sep=',')
    user_info = users_csv[users_csv['nom'] == name]
    user = Utilisateur_Existant(
        user_info['id'].values[0], 
        user_info['nom'].values[0], 
        user_info['date_naissance'].values[0], 
        user_info['role'].values[0], 
        user_info['date_enregistrement'].values[0],
        user_info['liste_livres'].values[0].split(',')
    )
    
    
    if user._role == 'Utilisateur':

        with st.sidebar:
            authenticator.logout('Se déconnecter', 'sidebar')

            st.markdown("---")

            st.markdown("## Modifier son profil")
            st.button('Modifier son mot de passe', key='change_password')
            st.button('Modifier son adresse mail', key='change_mail')
            st.button('Modifier son nom d\'utilisateur', key='change_username')
            st.button('Modifier sa date de naissance', key='change_birthdate')


        st.title(f'Bienvenue sur votre interface personnelle, *{name}*')

        st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True)

        # si l'utilisateur possède un livre, il l'affiche
        st.markdown("# MES LIVRES")

        if len(user._liste_livres) == 0:
            st.warning("Vous n'avez aucun livre en votre possession actuellement.")
        else:
            livres = pd.read_csv('books.csv', sep=',')
            livre_info = pd.DataFrame()
            for livre_index in user._liste_livres:
                livre_info = pd.concat([livres[livres['ID'] == int(livre_index)], livre_info], ignore_index=True)
            st.table(livre_info[['ID', 'Title', 'Author', 'Genre', 'Rating']].sort_values(by='ID', ascending=True).set_index('ID'))

        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
        st.markdown("---")

        action = st.selectbox(
            label="Que souhaitez-vous faire ?",
            options=['Rendre un livre', 'Emprunter un livre', 'Rechercher un livre', 'Voir les livres recommandés'],
            key='action'
        )



        ##### EMPRUNTER UN LIVRE #####
        if action == 'Emprunter un livre':
            st.markdown("---")
            st.markdown("## Emprunter un livre")
            # si l'utilisateur actif peut emprunter aujourd'hui 
            if len(user._liste_livres) < 6:
                st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)

                characteristic = st.selectbox(
                    label="Rechercher par...",
                    options=['Titre', 'Auteur', 'Genre', 'Éditeur'],
                    key='characteristic_emprunt'
                )
                value = st.text_input(
                    label=f'Rechercher un livre selon son {characteristic.lower()}',
                    key='value_emprunt',
                )
                
                
                if value and characteristic:
                    results = user.rechercher(value, characteristic)
                    results = results[results['Available'] == True]
                    if results.empty:
                        st.warning("Aucun résultat ne correspond à votre recherche.")
                    elif len(results) > 1:
                        st.warning(f"Votre recherche correspond à {len(results)} livres. Veuillez la préciser.")
                        st.write(results)
                    elif len(results) == 1:
                        st.success(f"Le livre \"{results['Title'].values[0]}\" est disponible. Empruntez-le !")
                        st.write(results)
                        if st.button('Emprunter ce livre'):
                            user.emprunter(results['ID'].values[0])
                            st.success(f"Vous avez emprunté le livre \"{results['Title'].values[0]}\" !")
                            sleep(2)
                            st.experimental_rerun()  
                    
            # si l'utilisateur possède déjà 5 (+1) livres
            else:
                st.warning("Vous avez déjà emprunté 5 livres. Vous ne pouvez plus en emprunter avant d'en rendre.")

        


        ##### RENDRE UN LIVRE #####
        elif action == 'Rendre un livre':
            st.markdown("---")
            st.markdown("## Retourner un livre")
            st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)

            if len(user._liste_livres) == 0:
                st.warning("Vous n'avez aucun livre en votre possession actuellement.")
            else:
                st.info("Pour information, la liste de vos livres est disponible ci-dessus.")
                characteristic = st.selectbox(
                    label="Rechercher par...",
                    options=['Titre', 'Auteur', 'Genre', 'Éditeur'],
                    key='characteristic_retourner'
                )
                value = st.text_input(
                    label=f'Rechercher un livre selon son {characteristic.lower()}',
                    key='value_retourner',
                )

                if value and characteristic:
                    results = user.rechercherDansListeUtilisateur(value, characteristic)
                    results = results[results['Title'] != "Fonctionnement de la bibliothèque"]
                    if results.empty:
                        st.warning("Aucun résultat ne correspond à votre recherche. Peut-être y a-t-il une faute de frappe ou un espace en trop ?")
                    elif len(results) > 1:
                        st.warning(f"Votre recherche correspond à {len(results)} livres. Veuillez la préciser.")
                        st.table(results)
                    elif len(results) == 1:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.success(f"Donnez une note à ce livre avant de le retourner !")
                        with col2:
                            note_livre = st.number_input('Note', min_value=0, max_value=5, value=0, step=1)
                        st.table(results)
                        if st.button('Retourner ce livre'):
                            user.retourner(results['ID'].values[0], note_livre)
                            st.success(f"Vous avez retourné le livre \"{results['Title'].values[0]}\" !")
                            sleep(2)
                            st.experimental_rerun()


        ##### RECHERCHER UN LIVRE #####
        elif action == 'Rechercher un livre':
            st.markdown("---")
            st.markdown("## Rechercher un livre")
            st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)

            characteristic_search = st.selectbox(
                label="Rechercher par...",
                options=['Titre', 'Auteur', 'Genre', 'Éditeur']
            )
            
            value_search = st.text_input(
                label=f'Rechercher un livre selon son {characteristic_search.lower()}'
            )
            
            if characteristic_search and value_search:
                resultats = user.rechercher(value_search, characteristic_search)
                resultats = resultats[resultats['Available'] == True]
                if resultats.empty:
                    st.warning("Aucun résultat ne correspond à votre recherche.")
                else:
                    st.write(resultats)
        


        ##### SYSTÈME DE RECOMMANDATION #####
        elif action == 'Voir les livres recommandés':
            st.markdown("---")
            st.markdown("## Système de recommandation de livres")
            st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)

            reco_sys = RecommenderSystem()

            number_recommended_books = st.slider("Nombre de livres", min_value=1, max_value=100, value=25, step=1)
            
            results_reco_sys = reco_sys.calculateTopK(user, number_recommended_books)
            results_reco_sys = results_reco_sys[results_reco_sys['Genre'] != "Règlement"]
            results_reco_sys = results_reco_sys[results_reco_sys['Available'] == True]
            if len(results_reco_sys) == 0:
                st.info("Aucun livre disponible ne correspond à vos lectures.")
            else:
                st.info("D'après vos lectures, voici les livres disponibles que nous vous recommandons")
                st.write(results_reco_sys[['Title', 'Author', 'Genre', 'Available', 'Mean_Rating', 'ID']])
    
    # si un admin est connecté
    else:
        
        users_csv = pd.read_csv('users.csv', sep=',')
        user_info = users_csv[users_csv['nom'] == name]
        admin = Admin_Existant(
            user_info['id'].values[0], 
            user_info['nom'].values[0], 
            user_info['date_naissance'].values[0], 
            user_info['role'].values[0], 
            user_info['date_enregistrement'].values[0],
        )

        st.title(f"Bienvenue sur l'interface d'administration, *{name}*")

        authenticator.logout('Se déconnecter', 'sidebar')

        admin_action = st.selectbox(
            label="Que souhaitez-vous faire ?",
            options=["Ajouter un livre", "Supprimer un livre", "Notifier l'utilisateur son temps d'emprunt"],
            key='admin_action'
        )

        if admin_action == "Ajouter un livre":
            st.markdown("---")
            st.markdown("## Ajouter un livre")
            st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                book_title = st.text_input("Titre du livre")
            with col2:
                book_author = st.text_input("Auteur du livre")
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                book_genre = st.text_input("Genre du livre")
            with sub_col2:
                book_publisher = st.text_input("Éditeur du livre")
            with sub_col3:
                book_height = st.number_input("Nombre de pages", min_value=0, max_value=1000, value=0, step=1)
            
            if book_title and book_author and book_genre and book_publisher and book_height:
                if st.button("Ajouter ce livre"):
                    admin.ajouterLivre(book_title, book_author, book_genre, book_publisher, book_height)
                    st.success(f"Le livre \"{book_title}\" a été ajouté avec succès !")
                    sleep(2)
                    st.experimental_rerun()
            else:
                st.warning("Veuillez remplir tous les champs.")



elif authentication_status == False:
    st.error("Le nom d'utilisateur ou le mot de passe est incorrect. Veuillez réessayer.")
elif authentication_status == None:
    st.info("Veuillez entrer vos identifiants pour accéder à l'interface de la bibliothèque.")

