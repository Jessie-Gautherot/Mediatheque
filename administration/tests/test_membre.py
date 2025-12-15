import pytest
from django.urls import reverse
from administration.models.membre import Membre

@pytest.mark.django_db
class TestMembre:

    def setup_method(self):
        # Crée un membre commun pour les tests
        self.membre = Membre.objects.create(
            nom="Doe",
            prenom="John",
            email="john@test.com",
            telephone="0123456789"
        )

    def teardown_method(self):
        # Nettoyage après chaque test
        Membre.objects.all().delete()

    # Vérifie l'ajout d'un membre via le formulaire et la vue
    def test_ajouter_membre(self, client):
        url = reverse('ajouter_membre')
        data = {
            'nom': 'Smith',
            'prenom': 'Anna',
            'email': 'anna.smith@example.com',
            'telephone': '0987654321'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Membre.objects.filter(email='anna.smith@example.com').exists()

    # Vérifie la modification d'un membre via la vue
    def test_modifier_membre_vue(self, client):
        url = reverse('modifier_membre', args=[self.membre.id])
        data = {
            'nom': 'Doe',
            'prenom': 'John',
            'email': 'john@doe.com',
            'telephone': '0123456789'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        self.membre.refresh_from_db()
        assert self.membre.email == 'john@doe.com'

    # Vérifie la suppression d'un membre via la vue
    def test_supprimer_membre_vue(self, client):
        url = reverse('supprimer_membre', args=[self.membre.id])
        response = client.post(url)
        assert response.status_code == 302
        assert not Membre.objects.filter(id=self.membre.id).exists()

    # Vérifie que la vue liste_membre retourne tous les membres
    def test_liste_membres_vue(self, client):
        Membre.objects.create(
            nom="Alice",
            prenom="Wonder",
            email="alice@example.com",
            telephone="0112233445"
        )
        url = reverse('liste_membres')
        response = client.get(url)
        assert response.status_code == 200

        membres = response.context['membres']
        noms = [m.nom for m in membres]
        prenoms = [m.prenom for m in membres]
        assert "Doe" in noms
        assert "Wonder" in prenoms
