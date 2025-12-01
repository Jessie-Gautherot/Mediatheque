from django.core.exceptions import ValidationError
from .models.emprunt import Emprunt

def creer_emprunt(membre, media):
    if not media.est_disponible():
        raise ValidationError("Media non disponible")
    if not membre.peut_emprunter():
        raise ValidationError("Ce membre ne peut pas emprunter")
    if not media.empruntable:
        raise ValidationError("Ce media n'est pas empruntable")
    return Emprunt.objects.create(membre=membre, media=media)
