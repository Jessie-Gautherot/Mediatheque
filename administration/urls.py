from django.urls import path
from .views.admin import admin_home, login_admin
from .views.medias import ajouter_livre, ajouter_cd, ajouter_dvd, ajouter_jeu


urlpatterns = [
    path('', admin_home, name='administration_home'),
    path('login/', login_admin, name='login_admin'),

    # Ajout de médias
    path('ajouter/livre/', ajouter_livre, name='ajouter_livre'),
    path('ajouter/cd/', ajouter_cd, name='ajouter_cd'),
    path('ajouter/dvd/', ajouter_dvd, name='ajouter_dvd'),
    path('ajouter/jeu/', ajouter_jeu, name='ajouter_jeu'),
]