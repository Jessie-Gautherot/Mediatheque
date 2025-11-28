from administration.models.media import Livre, CD, DVD, JeuDePlateau
from django.shortcuts import render




def liste_medias(request):
    livres = Livre.objects.all()
    cds = CD.objects.all()
    dvds = DVD.objects.all()
    jeux = JeuDePlateau.objects.all()
    liste_complete = list(livres) + list(cds) + list(dvds) + list(jeux)

    context = {
        "liste_livres": livres,
        "liste_cd": cds,
        "liste_dvd": dvds,
        "liste_jeux": jeux,
        "liste_complete": liste_complete,
    }

    return render(request, "home.html", context)


