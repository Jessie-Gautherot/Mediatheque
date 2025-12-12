from administration.models.media import Livre, CD, DVD, JeuDePlateau
from django.shortcuts import render

def liste_medias(request):

    livres = Livre.objects.all()
    cds = CD.objects.all()
    dvds = DVD.objects.all()
    jeux = JeuDePlateau.objects.all()
    liste_complete = list(livres) + list(cds) + list(dvds) + list(jeux)
    liste_empruntable = list(livres) + list(cds) + list(dvds)

    # Vérifie si le visiteur vient de la home pour avoir un lien retour
    from_visiteur = request.GET.get('from') == 'visiteur'


    context = {
        "liste_livres": livres,
        "liste_cd": cds,
        "liste_dvd": dvds,
        "liste_jeux": jeux,
        "liste_complete": liste_complete,
        "liste_empruntable": liste_empruntable,
        "from_visiteur": from_visiteur,
    }
    return render(request, "administration/liste_medias.html", context)