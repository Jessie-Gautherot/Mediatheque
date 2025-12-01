from django.db import models
from django.utils import timezone
from datetime import timedelta

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def emprunts_actifs(self):
        # Retourne tous les emprunts pas encore rendus par ce membre
        return self.emprunt_set.filter(date_retour__isnull=True)

    def a_emprunt_en_retard(self):
        # Vérifie si le membre a au moins un emprunt non rendu, dépassant la limite de 7 jours
        limite = timezone.now() - timedelta(days=7)
        return self.emprunt_set.filter(
            date_retour__isnull=True,
            date_emprunt__lt=limite
        ).exists()

    def peut_emprunter(self):
        # Vérifie si le membre peut emprunter : moins de 3 emprunts actifs et pas d’emprunt en retard
        return (
            self.emprunts_actifs().count() < 3
            and not self.a_emprunt_en_retard()
        )




