from django.db import models
from django.utils import timezone
from datetime import timedelta

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def emprunts_actifs(self):
        return self.emprunt_set.filter(date_retour__isnull=True)

    def emprunt_en_retard(self):
        limite = timezone.now() - timedelta(days=7)
        for emprunt in self.emprunts_actifs():
            if emprunt.date_emprunt < limite:
                return True
        return False

    def peut_emprunter(self):
        if not self.bloque and self.emprunts_actifs().count() < 3 and not self.emprunt_en_retard():
            return True
        else:
            return False




