from django import forms
from administration.models.media import Livre, CD, DVD, JeuDePlateau

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur']

class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['titre', 'artiste']

class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['titre', 'realisateur']

class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['titre', 'createur']