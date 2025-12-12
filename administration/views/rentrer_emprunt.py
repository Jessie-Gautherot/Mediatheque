from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from administration.models.media import Livre, CD, DVD, Media
from administration.models.membre import Membre
from administration.emprunt_service import creer_emprunt
from django.core.exceptions import ValidationError

# Afficher le formulaire de création d'un nouvel emprunt
def nouvel_emprunt(request):
    media_empruntables = list(Livre.objects.all()) + list(CD.objects.all()) + list(DVD.objects.all())
    membres = Membre.objects.all()
    return render(request, "administration/rentrer_emprunt.html", {
        "media_empruntables": media_empruntables,
        "membres": membres
    })

# Valider l'emprunt en utilisant le service
def valider_emprunt_multi(request):
    if request.method == "POST":
        membre = get_object_or_404(Membre, id=request.POST.get("membre_id"))
        media_ids = request.POST.getlist("media_ids")
        if not media_ids:
            messages.error(request, "Aucun média sélectionné.")
            return redirect("nouvel_emprunt")

        for media_id in media_ids:
            media = get_object_or_404(Media, id=media_id)
            try:
                creer_emprunt(membre, media)
                messages.success(request, f"{media} emprunté à {membre}.")
            except ValidationError as e:
                messages.error(request, f"{media} : {str(e)}")

    return redirect("nouvel_emprunt")
