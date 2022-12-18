import streamlit as st
import streamlit_authenticator as sa

from classes.utilisateur import Utilisateur_Nouveau

st.header("S'ENREGISTRER")

colu1, colu2 = st.columns([3, 1])
with colu1:
    placeholder_1 = st.empty()
    username = placeholder_1.text_input("Nom d'utilisateur")
with colu2:
    date_naissance = st.date_input("Date de naissance")

placeholder_2 = st.empty()
mail = placeholder_2.text_input("Adresse mail")

col1, col2 = st.columns(2)
with col1:
    placeholder_3 = st.empty()
    pwd = placeholder_3.text_input("Mot de passe", type="password")
with col2:
    placeholder_4 = st.empty()
    confirmed_pwd = placeholder_4.text_input("Confirmation du mot de passe", type="password")


if username and mail and pwd and confirmed_pwd:
    if pwd == confirmed_pwd:
        valider = st.button("VALIDER")

        if valider:
            user = Utilisateur_Nouveau(username, date_naissance)
            user.inscription(username, mail, sa.Hasher([pwd]).generate()[0])

            st.success(f"Bienvenue {username.upper()}, votre compte a été créé")

            username = placeholder_1.text_input("Nom d'utilisateur", value='', key=1)
            mail = placeholder_2.text_input("Adresse mail", value='', key=2)
            pwd = placeholder_3.text_input("Mot de passe", value='', key=3)
            confirmed_pwd = placeholder_4.text_input("Confirmation du mot de passe", value='', key=4)
else:
    st.info("Veuillez remplir tous les champs")


