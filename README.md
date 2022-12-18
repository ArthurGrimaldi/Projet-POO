# Bienvenue sur la Bibliothèque GEMA

Ce projet est un back office d'une bibliothèque permettant de
gérer les livres en tant qu'Admin, et de les utiliser
(emprunter/rendre) en tant qu'Utilisateur commun.

## Installation

Tous les packages sont disponibles dans le fichier requirements.txt

```
  pip install requirements.txt
```

## Utilisation

L'application est disponible à cette adresse : https://bastos-poo-gema.streamlit.app

Si le lien ne fonctionne pas, vous pouvez lancer l'application
avec cette commande :

```
streamlit run streamlit_home.py
```

Dirigez-vous sur la page "signup" si vous n'avez pas de compte,
puis vers la page "signin" pour vous y connecter.

Connectez-vous directement avec la page "signin" si vous possédez
déjà un compte chez nous.

#### Bienvenue !

Regardez votre liste, un livre est déjà présent : il contient les
règles d'utilisation de la bibliothèque. Lisez-le attentivement avant
toute action.

## UTILISATEUR COMMUN

### Rendre un livre

Cherchez un livre (parmi ceux que vous avez) selon différentes caractéristique (son titre, son auteur, son édition, son genre, etc).

Tant qu'il y aura plusieurs livres dans les résultats, l'action
de retour du livre ne sera pas disponible.
Il faut qu'il n'y ait **qu'un seul livre**. Enfin, le bouton pour rendre le livre apparaitra.

### Emprunter un livre

Même logique que pour retourner un livre.

### Chercher un livre

Logique de recherche classique.

### Système de recommandation de livres

Selon les livres que vous possédez actuellement, nous vous
proposons une liste de livres avec les mêmes genres en calculant
leur note moyenne.

## ADMINISTRATEUR

### Ajouter un livre

Renseignez les informations du livre.

### Retirer un livre

Même logique que pour emprunter, retourner ou rechercher un livre.
Filtrez les résultats jusqu'à qu'il ne reste plus **qu'un seul** livre.
