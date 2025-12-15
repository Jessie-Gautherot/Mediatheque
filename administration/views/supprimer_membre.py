from django.contrib import messages
from django.shortcuts import redirect

from administration.models import Membre


def supprimer_membre(request, membre_id):
    membre = Membre.objects.filter(id=membre_id).first()
    if not membre:
        messages.error(request, "Ce membre n'existe pas.")
        return redirect('liste_membres')

    # Vérifie si le membre a des emprunts actifs
    if membre.emprunts_actifs().exists():
        messages.error(
            request,
            "Impossible de supprimer : ce membre a encore des emprunts actifs."
        )
        return redirect('liste_membres')

    membre.delete()
    messages.success(request, "Membre supprimé avec succès.")
    return redirect('liste_membres')
