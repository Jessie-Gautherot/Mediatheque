from django.urls import path
from .views.admin import admin_home, login_admin
from .views.medias import ajouter_livre, ajouter_cd, ajouter_dvd, ajouter_jeu
from administration.views.ajouter_membre import ajouter_membre
from administration.views.liste_membres import liste_membres
from administration.views.modifier_membre import modifier_membre
from administration.views.liste_medias import liste_medias


urlpatterns = [

    # accueil et connexion
    path('', admin_home, name='administration_home'),
    path('login/', login_admin, name='login_admin'),

    # médias
    path("medias/", liste_medias, name="liste_medias"),
    path('ajouter/livre/', ajouter_livre, name='ajouter_livre'),
    path('ajouter/cd/', ajouter_cd, name='ajouter_cd'),
    path('ajouter/dvd/', ajouter_dvd, name='ajouter_dvd'),
    path('ajouter/jeu/', ajouter_jeu, name='ajouter_jeu'),

    # gestion des membres
    path('membres/', liste_membres, name='liste_membres'),
    path('membres/ajouter/', ajouter_membre, name='ajouter_membre'),
    path('membres/modifier/<int:membre_id>/', modifier_membre, name='modifier_membre'),
]