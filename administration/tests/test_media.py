import pytest
from django.urls import reverse
from administration.models.media import Livre, CD, DVD, JeuDePlateau

@pytest.mark.django_db
class TestMedia:

    # Vérifie que la vue 'liste_medias' retourne tous les médias créés
    def test_liste_complete_medias(self, client):
        Livre.objects.create(titre="Livre 1", auteur="Auteur 1")
        CD.objects.create(titre="CD 1", artiste="Artiste 1")
        DVD.objects.create(titre="DVD 1", realisateur="Réalisateur 1")
        JeuDePlateau.objects.create(titre="Jeu 1", createur="Créateur 1")

        url = reverse('liste_medias')
        response = client.get(url)

        liste_complete = response.context['liste_complete']
        titres = [m.titre for m in liste_complete]

        assert "Livre 1" in titres
        assert "CD 1" in titres
        assert "DVD 1" in titres
        assert "Jeu 1" in titres

    # Vérifie qu'un livre peut être ajouté via le formulaire et la vue
    def test_ajouter_livre(self, client):
        url = reverse('ajouter_livre')
        data = {
            'titre': 'Livre Vue',
            'auteur': 'Auteur Test'
        }

        response = client.post(url, data)

        assert Livre.objects.filter(titre='Livre Vue').exists()
        assert response.status_code == 302
