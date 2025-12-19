# Projet Mediatheque Django

## Description
Application de gestion d’une médiatheque : Programation orintée objet.

## Installation
1. Cloner le repo :
   git clone <https://github.com/Jessie-Gautherot/Mediatheque.git>
   cd <Mediatheque>

2. Installer les dépendances :
   pip install -r requirements.txt

3. Créer la base de données :
   python manage.py migrate

4. Charger les données de test :
   python manage.py loaddata administration/fixtures/data.json

5. Lancer le serveur :
   python manage.py runserver

6. Connexion à l’administration :
   - Username : Staff01
   - Password : media001