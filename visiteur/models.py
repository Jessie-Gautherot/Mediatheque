from django.db import models

class Media(models.Model):
    titre = models.CharField(max_length=200)
    date_emprunt = models.DateTimeField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(
        'administration.Emprunteur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        abstract = True


class Livre(Media):
    auteur = models.CharField(max_length=200)

    def __str__(self):
        return f"[Livre] {self.titre} écrit par {self.auteur}"


class CD(Media):
    artiste = models.CharField(max_length=200)

    def __str__(self):
        return f"[CD] {self.titre} de {self.artiste}"

class DVD(Media):
    realisateur = models.CharField(max_length=200)

    def __str__(self):
        return f"[DVD] {self.titre} de {self.realisateur}"


class JeuDePlateau(models.Model):
    titre = models.CharField(max_length=200)
    createur = models.CharField(max_length=200)

    def __str__(self):
        return f"[Jeu] {self.titre} créé par {self.createur}"






