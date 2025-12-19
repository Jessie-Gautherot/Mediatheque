# Dossier de projet – Médiathèque

## 1. Correctif du code existant

### Code initial
Le code fourni par le développeur initial n'était pas adapté à un projet Django  :   
- Les Classes comme `livre`, `cd`, `dvd`, `jeuDePlateau` et `Emprunteur` contenaient uniquement 
des variables (`name`, `dateEmprunt`, `disponible`, etc.) sans logique métier.  
- Classes et interface mélangées : le code gérait à la fois le menu et les données.

**Exemple :**

```python
class Livre:
    name = ""
    auteur = ""
    dateEmprunt = ""
    disponible = ""
    emprunteur = ""
```
### Correctifs apportés

**création de Modèles Django pour toutes les entités :**
- Media (classe mère)
- Livre
- CD
- DVD
- JeuDePlateau
- Membre
- Emprunt
Les relations sont gérées via des `ForeignKey`, il n'y a plus besoin de variables manuelles 
comme `emprunteur` ou `disponible`

**Centralisation de la logique métier :**
- Les modèles contiennent toutes les règles métier :
  - `Media.est_disponible()`
  - `Membre.peut_emprunter()`
  - `Membre.a_emprunt_en_retard()`
  - `Emprunt.est_en_retard()`
  - `Emprunt.enregistrer_retour()`

**Services pour l’orchestration :**
- Le fichier `emprunt_service.py` contient des fonctions comme :
  - `creer_emprunt()`
  - `enregistrer_retour_emprunt()`
- Ces fonctions :
  - Appellent les méthodes des modèles pour appliquer la logique métier
  - Gèrent les exceptions et la validation
  - Permettent aux vues de rester légères et centrées sur l’interface et le flux HTTP

**Vues légères :**
- Récupèrent les données
- Appellent le service approprié
- Affichent les messages à l’utilisateur

**Templates :**
- Affichage HTML
- Gestion des formulaires
- Affichage des messages d’erreur

**2. Mise en place des fonctionnalités demandées**

***2.1 Modèles (Models)***

- Logique métier centralisée pour réutilisabilité et lisibilité
  - `Emprunt` : sait s’il est actif ou en retard (`est_en_retard()`), peut enregistrer son retour
  (`enregistrer_retour()`)
  - `Membre` : sait s’il peut emprunter (`peut_emprunter()`), connaît ses emprunts actifs
  (`emprunts_actifs()`) et les retards (`a_emprunt_en_retard()`)
  - `Media` et sous-classes : sait s’il est disponible (`est_disponible()`). 
  Les jeux de plateau sont jouables sur place uniquement (`empruntable=False`)
- Principe SRP : chaque modèle gère sa logique propre, sans dépendre des autres objets


- Exemple d’utilisation dans une vue :

    if membre.peut_emprunter():
        creer_emprunt(membre, media)

Les vues restent légères, elles orchestrent les objets sans recalculer la logique métier.


***2.2 Services (emprunt_service)***

- **Orchestration des objets et application des règles métier complexes**

- **Création d’emprunt (`creer_emprunt`)**  
  Vérifie la disponibilité du média et la capacité du membre avant de créer l’emprunt

- **Retour d’emprunt (`enregistrer_retour_emprunt`)**  
  Vérifie que l’emprunt n’est pas déjà rendu, puis enregistre la date de retour

- **Avantage**  
  Centralisation de la logique métier, vues simples et claires

***2.3 Views et Templates***

****Views****

- Respect du SRP
  Chaque vue respecte le Single Responsibility Principle : affichage (GET) ou traitement (POST)

- CRUD Media et Membres
  - ajouter_livre  
  - ajouter_cd  
  - ajouter_dvd  
  - ajouter_jeu  
  - ajouter_membre  
  - modifier_membre  
  - supprimer_membre

- Emprunt / Retour
  - nouvel_emprunt  
  - valider_emprunt_multi  
  - retourner_media  
  - valider_retour_multi

- Gestion des erreurs
  Utilisation de Django messages (`success` / `error`)

****Templates****

- HTML simple et épuré 
  Titre, formulaire ou liste d’objets (`{{ form.as_p }}` ou boucles QuerySet)

- Boutons d’action 
  Pour soumettre ou revenir à l’espace précédent

- CSS minimal

- Exemples
  - Ajout de média/membre : `<h1>Ajouter un {{ type_media }}</h1>`, formulaire généré automatiquement, bouton “Enregistrer”, lien retour  
  - Liste de médias/membres : boucles sur QuerySet, filtre par type  
  - Emprunt / Retour : checkboxes pour sélectionner les médias disponibles à l'emprunt
et les emprunts actifs du membre concerné.
  
***2.4 Flux Emprunt / Retour***

****Emprunt****

**GET : affichage des membres et des médias disponibles**

```python
media_empruntables = [
    media for media in Livre.objects.all() + CD.objects.all() + DVD.objects.all()
    if media.est_disponible()
]
```

**POST : création des emprunts via `creer_emprunt()`**  
  - Vérification que le membre et les médias existent  
  - Messages de succès ou d’erreur, puis redirection

****Retour***

- **GET : sélection d’un membre et affichage de ses emprunts actifs**

- **POST : appel de `enregistrer_retour_emprunt()`**  
  - Messages de succès ou d’erreur, puis redirection

- **Avantages**  
  - Sécurité et cohérence  
  - Séparation claire des responsabilités :  
    - Modèle → logique métier (`est_disponible()`, `enregistrer_retour()`)  
    - Vue → préparation des données  
    - Template → affichage et interaction utilisateur
    
***2.5 Gestion des erreurs***

- Messages d’erreur 
  Pour informer l’utilisateur

- Règles métier centralisées
  Dans les modèles ou services

- Vues responsables uniquement de l’affichage et de la redirection


***2.6 URLs***

- **Chaque action CRUD possède une URL claire et descriptive :**
  - `/admin/ajouter/livre/` → `ajouter_livre`  
  - `/admin/ajouter/cd/` → `ajouter_cd`  
  - `/admin/ajouter/dvd/` → `ajouter_dvd`  
  - `/admin/ajouter/jeu/` → `ajouter_jeu`


***2.7 Choix de développement***

- Code simple et lisible
- Chaque méthode fait une seule chose et est réutilisable
- Centralisation de la logique métier dans modèles et services
- Vues légères et templates épurés
- Interfaces simples et intuitives pour les utilisateurs (bibliothécaires)


**3 Tests**

J’ai combiné tests manuels et automatisés avec Pytest pour vérifier que toutes les fonctionnalités
essentielles pour l’utilisateur (bibliothécaire) sont opérationnelles. 
Les tests couvrent le parcours complet : interface → vue → service → modèles.


****3.1 Tests d’intégration****

- **Vérification du parcours complet**  
  Les tests vérifient le parcours complet d’une action utilisateur sur une base de test 
  isolée (`pytest.mark.django_db`)

- **Simulation de requêtes HTTP**  
  Utilisation de `client.get()` ou `client.post()` pour tester les vues et formulaires 
  comme un utilisateur réel

- **Exemple : ajout d’un média via formulaire**

```python
url = reverse('ajouter_livre')
data = {'titre': 'Livre Test', 'auteur': 'Auteur Test'}
response = client.post(url, data)
assert response.status_code == 302
assert Livre.objects.filter(titre='Livre Test').exists() 
```

Ici, `client.post()` simule l’envoi du formulaire, et l’assertion vérifie que le média 
a bien été ajouté dans la base de test.

- **Autres exemples testés**  
  - Emprunts : création et retour via service et vues  
  - Membre : création, modification, suppression et affichage de la liste

Ces tests garantissent que les fonctionnalités essentielles pour l’utilisateur sont 
correctement implémentées et fonctionnent ensemble de manière cohérente.


***3.2 Test unitaire***

J’ai ajouté un test unitaire spécifique pour tester de manière isolée une fonction importante 
du service : la création d’un emprunt.

```python
membre = mocker.Mock(peut_emprunter=lambda x=1: True)
media = mocker.Mock(est_disponible=lambda: True, empruntable=True)
mock_create = mocker.patch(
    "administration.emprunt_service.Emprunt.objects.create",
    return_value=mocker.MagicMock(date_retour=None)
)

emprunt = creer_emprunt(membre, media)
assert emprunt.date_retour is None
mock_create.assert_called_once_with(membre=membre, media=media)
```

Ici, `mocker.Mock` permet de simuler un membre et un média avec le comportement souhaité, 
sans toucher à la vraie base.  
`mocker.patch` remplace temporairement la méthode `Emprunt.objects.create` 
pour vérifier qu’elle est bien appelée avec les bons arguments.  

Ce test vérifie la logique métier indépendamment de la base de données ou des vues, et 
s’assure que les règles (disponibilité du média, quota du membre) sont respectées.


***3.3 Choix méthodologiques***

- Couverture ciblée 
  Les tests d’intégration garantissent le bon fonctionnement global, 
  tandis que le test unitaire cible la logique métier

- Fiabilité
  La combinaison de base simulée, de mocks et de tests automatisés permet de détecter 
  rapidement les erreurs.


***4 Base de données***

Le projet utilise SQLite3 comme base de données. Comme le fichier de base de données SQLite 
ne peut pas être directement partagé sur GitHub de manière fiable, j’ai exporté les données 
de test dans une fixture au format JSON.  

Cette fixture contient tous les objets nécessaires pour tester le fonctionnement 
de l’application : membres, médias, emprunts. Elle permet au correcteur de repeupler 
la base de données en exécutant la commande :
```bash
python manage.py loaddata administration/fixtures/data.json
````

***5 Instructions d’exécution depuis GitHub***

- **a/ Cloner le repository**
```bash
git clone https://github.com/Jessie-Gautherot/Mediatheque
cd Mediatheque
````

- **b/ Installer les dépendances**  
Assurez-vous que Python et Django sont installés. Puis :
```bash
pip install -r requirements.txt
````

- **c/ Recréer la base de données**  
Appliquez les migrations pour créer les tables :
```bash
python manage.py migrate
````

- **d/ Insérer les données de test**  
Chargez la fixture JSON fournie pour peupler la base avec les données de test :
```bash
python manage.py loaddata administration/fixtures/data.json
````

- **e/ Lancer le serveur de développement**
```bash
python manage.py runserver
````

- **f/ Connexion à l’interface d’administration**  
Nom d’utilisateur : `Staff01`  
Mot de passe : `media001`


- **g/ Lancer les tests**  
Le projet s’appelle `Mediatheque` avec un M majuscule. Django et pytest-django sont 
sensibles à la casse, il est donc important de spécifier correctement le chemin et le 
module de settings avant de lancer les tests.  

Sous Windows PowerShell, procédez ainsi :

```bash
# Indiquer le chemin vers le projet
$env:PYTHONPATH = "C:\Users\User\Desktop\Mediatheque"

# Spécifier le module de settings de Django
$env:DJANGO_SETTINGS_MODULE = "Mediatheque.settings"

# Lancer les tests sur le fichier test_emprunt.py en mode verbeux
python -m pytest administration/tests/test_emprunt.py -v
```

**Explications :**  
- `$env:PYTHONPATH` : permet à Python de trouver le projet `Mediatheque`.  
- `$env:DJANGO_SETTINGS_MODULE` : indique à Django quel fichier de settings utiliser.  
- `-v` : active le mode verbeux de pytest pour voir le détail de chaque test.  

Cette configuration garantit que les tests s’exécutent correctement, même si le nom du projet
contient une majuscule.





