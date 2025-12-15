from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .media import Media
from .membre import Membre


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)

    # Vérifie si l'emprunt est en retard
    def est_en_retard(self):
        if self.date_retour:
            return False
        limite = self.date_emprunt + timedelta(days=7)
        return timezone.now() > limite

    # Enregistre le retour de l'emprunt
    def enregistrer_retour(self):
        if self.date_retour is not None:
            raise ValidationError("Ce média a déjà été rendu.")
        self.date_retour = timezone.now()
        self.save()
        return self


