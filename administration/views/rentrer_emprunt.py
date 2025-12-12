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
    if request.method != "POST":
        return redirect("nouvel_emprunt")

    membre_id = request.POST.get("membre_id")
    media_ids = request.POST.getlist("media_ids")


    if not membre_id:
        messages.error(request, "Aucun membre sélectionné.")
        return redirect("nouvel_emprunt")

    membre = get_object_or_404(Membre, id=membre_id)

    if not media_ids:
        messages.error(request, "Aucun média sélectionné.")
        return redirect("nouvel_emprunt")

    emprunts_actifs = membre.emprunts_actifs().count()
     # Vérification de la limite de 3 médias
    if emprunts_actifs + len(media_ids) > 3:
        messages.error(
            request,
            f"Limite de 3 médias dépassée. Ce membre a déjà {emprunts_actifs} emprunt(s) actif(s). "
            f"Il ne peut emprunter que {3 - emprunts_actifs} média(s) supplémentaire(s)."
        )
        return redirect("nouvel_emprunt")

    # Boucle pour créer chaque emprunt via le service
    for media_id in media_ids:
        media = get_object_or_404(Media, id=media_id)
        try:
            # On passe nb_media=1 pour chaque création individuelle
            creer_emprunt(membre, media, nb_media=1)
        except ValidationError as e:
            messages.error(request, f"{media} : {str(e)}")

    messages.success(request, 'emprunt enregistré')
    return redirect("nouvel_emprunt")