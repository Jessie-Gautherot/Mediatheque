from django.shortcuts import render, redirect
from administration.forms.form_media import LivreForm, CDForm, DVDForm, JeuDePlateauForm

# Fonction pour ajouter n'importe quel type de média
def ajouter_media(request, form_class, type_media):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_home')
    else:
        form = form_class()

    return render(request, "administration/ajouter_media.html", {
        "form": form,
        "type_media": type_media
    })


# Fonctions spécifiques pour les URLs
def ajouter_livre(request):
    return ajouter_media(request, LivreForm, "Livre")

def ajouter_cd(request):
    return ajouter_media(request, CDForm, "CD")

def ajouter_dvd(request):
    return ajouter_media(request, DVDForm, "DVD")

def ajouter_jeu(request):
    return ajouter_media(request, JeuDePlateauForm, "Jeu")
