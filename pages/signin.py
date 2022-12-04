import streamlit as st 
import streamlit_authenticator as stauth
import yaml
import pandas as pd

from classes.utilisateur import Utilisateur_Existant

  

with open('config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    users_csv = pd.read_csv('users.csv', sep=',')
    user_info = users_csv[users_csv['nom'] == name]
    user = Utilisateur_Existant(
        user_info['id'].values[0], 
        user_info['nom'].values[0], 
        user_info['date_naissance'].values[0], 
        user_info['statut'].values[0], 
        user_info['date_enregistrement'].values[0],
        # user_info['emprunt_jour'].values[0],
        True,
        user_info['liste_livres'].values[0].split(',')
    )
    
    with st.sidebar:
        authenticator.logout('Se déconnecter', 'main')

        st.markdown("---")

        st.markdown("## Modifier son profil")
        st.button('Modifier son mot de passe', key='change_password')
        st.button('Modifier son adresse mail', key='change_mail')
        st.button('Modifier son nom d\'utilisateur', key='change_username')
        st.button('Modifier sa date de naissance', key='change_birthdate')


    st.title(f'Bienvenue sur votre interface personnelle, *{name}*.')


    # create div for blank space
    st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True)

    # si l'utilisateur possède un livre, il l'affiche
    st.markdown("# MES LIVRES")

    if len(user._liste_livres) == 0:
        st.write("Vous n'avez aucun livre en votre possession actuellement.")
    else:
        livres = pd.read_csv('books.csv', sep=',')
        livre_info = pd.DataFrame()
        for livre_index in user._liste_livres:
            livre_info = pd.concat([livres[livres['ID'] == int(livre_index)], livre_info], ignore_index=True)
        livre_info["Date d'emprunt"] = 'à rajouter'
        st.write(livre_info[['ID', 'Title', 'Author', 'Genre', 'Date d\'emprunt']])

        st.markdown("---")
        st.markdown("## Emprunter un livre")
        # si l'utilisateur actif peut emprunter aujourd'hui 
        if user._emprunt_jour or len(user._liste_livres) < 5:
            st.markdown('<div style="height: 30;"></div>', unsafe_allow_html=True)

            characteristic = st.selectbox(
                label="Rechercher par...",
                options=['Titre', 'Auteur', 'Genre', 'Éditeur'],
                key='characteristic_emprunt'
            )
            value = st.text_input(
                label=f'Rechercher un livre selon son {characteristic.lower()}',
                key='value_emprunt'
            )
            results = user.rechercher(value, characteristic)
            results = results[results['Available'] == True]
            if st.button('Rechercher', key='search_emprunt'):
                if len(results) == 0:
                    st.warning("Aucun résultat ne correspond à votre recherche.")
                elif len(results) > 1:
                    st.warning(f"Votre recherche correspond à {len(results)} livres. Veuillez la préciser.")
                    st.write(results)
                else:
                    st.success(f"Le livre \"{results['Title'].values[0]}\" est disponible. Empruntez-le !")
                    st.write(results)
                    if st.button('Emprunter ce livre'):
                        user.emprunter(results['ID'].values[0])
        else:
            st.warning("Vous avez déjà emprunté un livre aujourd'hui ou vous en avez trop emprunté. Revenez demain ou rendez en un !")
    

    # st.markdown("## Retourner un livre")
    # st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


    # st.markdown("## Rechercher un livre")
    # characteristic = st.selectbox(
    #     label="Rechercher par...",
    #     options=['Titre', 'Auteur', 'Genre', 'Éditeur']
    # )
    # # if characteristic == 'Disponibilité':
    # #     dispo = st.selectbox(
    # #         label="Rechercher un livre selon sa disponibilité",
    # #         options=['Disponible', 'Non disponible']
    # #     )
    # #     if dispo == 'Disponible':
    # #         value = True
    # #     else:
    # #         value = False
    # # else:
    # value = st.text_input(
    #     label=f'Rechercher un livre selon son {characteristic.lower()}'
    # )
    
    # if st.button('Rechercher', key='search_book'):
    #     st.write(user.rechercher(value, characteristic))
        
    


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

