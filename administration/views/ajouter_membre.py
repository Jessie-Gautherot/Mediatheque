from django.shortcuts import render, redirect
from administration.models import Membre
from administration.forms.form_membre import MembreForm
from django.contrib import messages

def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre ajouté avec succès !")
            return redirect('liste_membres')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreForm()

    return render(request, 'administration/ajouter_membre.html', {'form': form, })
