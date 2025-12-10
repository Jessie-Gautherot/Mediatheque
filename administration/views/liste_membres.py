from django.shortcuts import render
from administration.models import Membre

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'administration/liste_membres.html', {'membres': membres})
