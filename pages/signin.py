import streamlit as st 
import streamlit_authenticator as stauth
import yaml
import pandas as pd

from classes.utilisateur import Utilisateur, Utilisateur_Existant

# st.header("SE CONNECTER")

# names = ['John Smith','Rebecca Briggs']
# usernames = ['jsmith','rbriggs']
# passwords = ['123','456']

# hashed_passwords = stauth.Hasher(passwords).generate()

# passwords = hashed_passwords    

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
        user_info['emprunt_jour'].values[0],
        user_info['liste_livres'].values[0]
    )

    with st.sidebar:
        authenticator.logout('Se déconnecter', 'main')

        st.markdown("---")

        st.markdown("## Modifier son profil")
        st.button('Modifier son mot de passe')
        st.button('Modifier son adresse mail')
        st.button('Modifier son nom d\'utilisateur')
        st.button('Modifier sa date de naissance')


    st.title(f'Welcome *{name}*')


    # create div for blank space
    st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)


    st.markdown("# MES LIVRES")
    st.markdown(user.liste_livres)



    st.markdown("## Emprunter un livre")
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


    st.markdown("## Retourner un livre")
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


    st.markdown("## Rechercher un livre")
    characteristic = st.selectbox(
        label="Rechercher par...",
        options=['Titre', 'Auteur', 'Genre', '  Éditeur', 'Disponibilité']
    )
    st.text_input(
        label=f'Rechercher un livre selon son {characteristic.lower()}' if characteristic != 'Disponibilité' else 'Rechercher un livre selon sa disponibilité'
    )
    st.button('Rechercher')
    


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

