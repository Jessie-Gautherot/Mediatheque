from administration.models.media import Livre, CD, DVD, JeuDePlateau
from django.shortcuts import render

def liste_medias(request):
    medias_par_type = {
        "Livres": Livre.objects.all(),
        "CD": CD.objects.all(),
        "DVD": DVD.objects.all(),
        "Jeux de plateau": JeuDePlateau.objects.all(),
    }

    liste_complete = list(Livre.objects.all()) + list(CD.objects.all()) + list(DVD.objects.all()) + list(JeuDePlateau.objects.all())

    from_visiteur = request.GET.get('from') == 'visiteur'

    return render(request, "administration/liste_medias.html", {
        "medias_par_type": medias_par_type,
        "liste_complete": liste_complete,
        "from_visiteur": from_visiteur,
    })
