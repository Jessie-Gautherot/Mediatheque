from django.contrib import messages
from django.shortcuts import redirect, render

from administration.forms.form_membre import MembreForm


def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre ajouté avec succès !")
            return redirect(request.path)
        else:
            messages.error(
                request,
                "Veuillez corriger les erreurs dans le formulaire."
            )
    else:
        form = MembreForm()

    return render(
        request,
        'administration/ajouter_membre.html',
        {'form': form},
    )
