from django.shortcuts import render, redirect
from administration.forms import LivreForm, CDForm, DVDForm, JeuDePlateauForm

def ajouter_livre(request):
    if request.method == "POST":
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('administration_home')
    else:
        form = LivreForm()
    return render(request, "administration/ajouter_media.html", {"form": form, "type_media": "Livre"})

def ajouter_cd(request):
    if request.method == "POST":
        form = CDForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('administration_home')
    else:
        form = CDForm()
    return render(request, "administration/ajouter_media.html", {"form": form, "type_media": "CD"})

def ajouter_dvd(request):
    if request.method == "POST":
        form = DVDForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_home')
    else:
        form = DVDForm()
    return render(request, "administration/ajouter_media.html", {"form": form, "type_media": "DVD"})

def ajouter_jeu(request):
    if request.method == "POST":
        form = JeuDePlateauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_home')
    else:
        form = JeuDePlateauForm()
    return render(request, "administration/ajouter_media.html", {"form": form, "type_media": "Jeu"})
