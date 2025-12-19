from django import forms
from administration.models import Membre

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'telephone']
