from django.core.exceptions import ValidationError
from .models.emprunt import Emprunt

# Création d'un emprunt
def creer_emprunt(membre, media):
    if not media.est_disponible():
        raise ValidationError("Media non disponible")
    if not membre.peut_emprunter():
        raise ValidationError("Ce membre ne peut pas emprunter")
    if not media.empruntable:
        raise ValidationError("Ce media n'est pas empruntable")
    return Emprunt.objects.create(membre=membre, media=media)

# Récupère les emprunts actifs d’un membre par son id
def get_emprunts_actifs_par_membre_id(membre_id):
    return Emprunt.objects.filter(
        membre_id=membre_id,
        date_retour__isnull=True
    )

# Enregistre le retour d’un emprunt unique
def enregistrer_retour_emprunt(emprunt_id):
        try:
            emprunt = Emprunt.objects.get(id=emprunt_id, date_retour__isnull=True)
            emprunt.enregistrer_retour()
            return emprunt
        except Emprunt.DoesNotExist:
            raise ValidationError(f"Emprunt {emprunt_id} introuvable ou déjà rendu.")