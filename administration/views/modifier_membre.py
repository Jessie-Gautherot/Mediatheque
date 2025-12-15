from django.contrib import messages
from django.shortcuts import redirect, render

from administration.forms.form_membre import MembreForm
from administration.models import Membre


def modifier_membre(request, membre_id):
    # Récupère le membre ou None si inexistant
    membre = Membre.objects.filter(id=membre_id).first()
    if not membre:
        messages.error(request, "Ce membre n'existe pas.")
        return redirect('liste_membres')  # arrête la fonction et redirige

    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre modifié avec succès !")
            return redirect('liste_membres')  # arrête la fonction après succès
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreForm(instance=membre)

    # Rend la page avec le formulaire pré-rempli
    return render(
        request,
        'administration/modifier_membre.html',
        {
            'form': form,
            'membre': membre,
        },
    )
