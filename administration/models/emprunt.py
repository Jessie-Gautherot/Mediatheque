from django.db import models
from django.utils import timezone
from datetime import timedelta
from .membre import Membre
from .media import Media

class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)

    def est_en_retard(self):
        # Retourne true si le média n'a pas encore été rendu et que l'emprunt dépasse la limite
        if self.date_retour:
            return False
        date_limite = self.date_emprunt + timedelta(days=7)
        if timezone.now() > date_limite:
            return True
        else:
            return False

