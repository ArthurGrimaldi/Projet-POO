import streamlit as st
import streamlit_authenticator as sa

from classes.utilisateur import Utilisateur_Nouveau


st.title("Bienvenue sur la Bibliothèque GEMA")
st.write("Connectez-vous ou enregistrez-vous pour accéder à votre bibliothèque")


# st.write("S'enregistrer")

# colu1, colu2 = st.columns([3, 1])
# with colu1:
#     placeholder_1 = st.empty()
#     username = placeholder_1.text_input("Nom d'utilisateur")
# with colu2:
#     date_naissance = st.date_input("Date de naissance")

# placeholder_2 = st.empty()
# mail = placeholder_2.text_input("Adresse mail")

# col1, col2 = st.columns(2)
# with col1:
#     placeholder_3 = st.empty()
#     pwd = placeholder_3.text_input("Mot de passe")
# with col2:
#     placeholder_4 = st.empty()
#     confirmed_pwd = placeholder_4.text_input("Confirmation du mot de passe")

# footer1, footer2 = st.columns([6, 1])
# with footer2 :
#     valider = st.button("VALIDER")
# if valider:
#     user = Utilisateur_Nouveau(username, date_naissance)
#     user.inscription(username, mail, pwd)

#     st.success(f"Bienvenue {username.upper()}, votre compte a été créé")

#     username = placeholder_1.text_input("Nom d'utilisateur", value='', key=1)
#     mail = placeholder_2.text_input("Adresse mail", value='', key=2)
#     pwd = placeholder_3.text_input("Mot de passe", value='', key=3)
#     confirmed_pwd = placeholder_4.text_input("Confirmation du mot de passe", value='', key=4)


