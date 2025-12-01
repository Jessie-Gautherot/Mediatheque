from django.db import models

class Media(models.Model):
    titre = models.CharField(max_length=200)
    empruntable = models.BooleanField(default=True)


    def est_disponible(self):
        # Vérifie s’il n’existe pas d’emprunt en cours pour ce média
        emprunts_actifs = self.emprunt_set.filter(date_retour__isnull=True)
        if emprunts_actifs.exists():
            return False
        else:
            return True

    def __str__(self):
        return self.titre


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
    empruntable = models.BooleanField(default=False)

    def __str__(self):
        return f"[Jeu] {self.titre} créé par {self.createur}"
