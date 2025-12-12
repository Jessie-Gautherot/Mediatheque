from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from administration.models.membre import Membre
from administration.emprunt_service import (get_emprunts_actifs_par_membre_id,enregistrer_retour_emprunt)
from django.core.exceptions import ValidationError


# Affiche la page pour choisir un membre et voir ses emprunts actifs
def retourner_media(request) :
    membres = Membre.objects.all()
    emprunts = None

    # Si un membre est sélectionné, on charge ses emprunts actifs
    membre_id = request.GET.get("membre_id")
    if membre_id:
        emprunts = get_emprunts_actifs_par_membre_id(membre_id)

    return render(request, "administration/rentrer_retour.html", {
        "membres": membres,
        "emprunts": emprunts,
        "membre_id": membre_id,
    })


# Valide le retour de plusieurs emprunts
def valider_retour_multi(request):
    if request.method == "POST":
        emprunt_ids = request.POST.getlist("emprunt_ids")

        if not emprunt_ids:
            messages.error(request, "Aucun emprunt sélectionné.")
            return redirect("retourner_media")

        for emprunt_id in emprunt_ids:
            try:
                enregistrer_retour_emprunt(emprunt_id)
                messages.success(request, f"Emprunt {emprunt_id} rendu.")
            except ValidationError as e:
                messages.error(request, str(e))

    return redirect("retourner_media")
