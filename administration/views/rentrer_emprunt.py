from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render

from administration.emprunt_service import creer_emprunt
from administration.models.media import CD, DVD, Livre, Media
from administration.models.membre import Membre


# Afficher le formulaire de création d'un nouvel emprunt
def nouvel_emprunt(request):
    media_empruntables = (
        list(Livre.objects.all())
        + list(CD.objects.all())
        + list(DVD.objects.all())
    )
    membres = Membre.objects.all()
    return render(
        request,
        "administration/rentrer_emprunt.html",
        {
            "media_empruntables": media_empruntables,
            "membres": membres,
        },
    )


# Valider l'emprunt en utilisant le service
def valider_emprunt_multi(request):
    if request.method != "POST":
        return redirect("nouvel_emprunt")

    membre_id = request.POST.get("membre_id")
    media_ids = request.POST.getlist("media_ids")

    membre = Membre.objects.filter(id=membre_id).first()
    if not membre:
        messages.error(request, "Ce membre n'existe pas.")
        return redirect("nouvel_emprunt")

    if not media_ids:
        messages.error(request, "Aucun média sélectionné.")
        return redirect("nouvel_emprunt")

    # Vérification de la limite de 3 médias
    emprunts_actifs = membre.emprunts_actifs().count()
    if emprunts_actifs + len(media_ids) > 3:
        messages.error(
            request,
            (
                f"Limite de 3 médias dépassée. Ce membre a déjà {emprunts_actifs} "
                f"emprunt(s) actif(s). Il ne peut emprunter que {3 - emprunts_actifs} "
                "média(s) supplémentaire(s)."
            ),
        )
        return redirect("nouvel_emprunt")

    # Boucle pour créer chaque emprunt via le service
    succes = 0

    for media_id in media_ids:
        media = Media.objects.filter(id=media_id).first()
        if not media:
            messages.error(request, f"Média {media_id} introuvable.")
            continue

        try:
            creer_emprunt(membre, media, nb_media=1)
            succes += 1
        except ValidationError as e:
            messages.error(request, f"{media} : {str(e)}")

    # Message final cohérent
    if succes > 0:
        messages.success(
            request,
            f"{succes} emprunt(s) enregistré(s) avec succès."
        )
    else:
        messages.error(
            request,
            "Aucun emprunt n'a pu être enregistré."
        )

    return redirect("nouvel_emprunt")