import streamlit as st 
import streamlit_authenticator as stauth
import yaml

from classes.utilisateur import Utilisateur

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


    search_button = False



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
    st.button('Rechercher', on_click=search_book(search_button))
    


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

