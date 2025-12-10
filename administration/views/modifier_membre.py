from django.shortcuts import render, redirect
from administration.models import Membre
from administration.forms.form_membre import MembreForm
from django.contrib import messages

def modifier_membre(request, membre_id):
    # Cherche le membre, renvoie None si pas trouvé
    membre = Membre.objects.filter(id=membre_id).first()
    if not membre:
        messages.error(request, "Ce membre n'existe pas.")
        return redirect('liste_membres')

    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre modifié avec succès !")
            return redirect('liste_membres')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreForm(instance=membre)

    return render(request, 'administration/modifier_membre.html', {'form': form})
