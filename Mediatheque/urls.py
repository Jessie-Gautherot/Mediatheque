from django.contrib import admin
from django.urls import path, include
from .views import home


urlpatterns = [
    path('', home, name='home'),  # Page d’accueil
    path('visiteur/', include('visiteur.urls')),
    path('administration/', include('administration.urls')),
    path('admin/', admin.site.urls),
]

