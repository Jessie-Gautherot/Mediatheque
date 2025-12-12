from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from administration.models import Membre

def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)

    if membre.emprunts_actifs().exists():
        messages.error(request, "Impossible de supprimer : ce membre a encore des emprunts actifs.")
        return redirect('liste_membres')

    membre.delete()
    messages.success(request, "Membre supprimé avec succès.")
    return redirect('liste_membres')

