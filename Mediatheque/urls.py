from django.contrib import admin
from django.urls import path, include
from .views import home


urlpatterns = [
    path('', include('visiteur.urls')),
    path('administration/', include('administration.urls')),
    path('admin/', admin.site.urls),
]

