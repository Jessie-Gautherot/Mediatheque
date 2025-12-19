import pytest
from django.urls import reverse
from administration.models.membre import Membre
from administration.models.media import Livre, CD, DVD
from administration.models.emprunt import Emprunt
from administration.emprunt_service import creer_emprunt

@pytest.mark.django_db
class TestEmprunt:

    def setup_method(self, method):
        # Création d'un membre et de médias pour les tests
        self.membre = Membre.objects.create(
            nom="Test",
            prenom="Anna",
            email="test@anna.com",
            telephone="0123456789"
        )
        self.livre = Livre.objects.create(titre="Livre Test", empruntable=True)
        self.cd = CD.objects.create(titre="CD Test", empruntable=True)
        self.dvd = DVD.objects.create(titre="DVD Test", empruntable=True)

    def teardown_method(self, method):
        # Nettoyage après chaque test
        Emprunt.objects.all().delete()
        Livre.objects.all().delete()
        CD.objects.all().delete()
        DVD.objects.all().delete()
        Membre.objects.all().delete()

    # Teste la création d'un emprunt via la vue et le service
    def test_creer_emprunt(self, client):
        url = reverse('valider_emprunt_multi')
        data = {
            'membre_id': self.membre.id,
            'media_ids': [self.livre.id]
        }
        response = client.post(url, data)

        assert response.status_code == 302
        emprunt = Emprunt.objects.filter(membre=self.membre, media=self.livre).first()
        assert emprunt is not None
        assert emprunt.date_retour is None

    # Teste le retour d'un emprunt via le service et la vue
    def test_retourner_emprunt(self, client):
        # Création d'un emprunt
        emprunt = Emprunt.objects.create(membre=self.membre, media=self.livre)

        url = reverse('valider_retour_multi')
        data = {
            'emprunt_ids': [emprunt.id]
        }
        response = client.post(url, data)

        assert response.status_code == 302
        emprunt.refresh_from_db()
        assert emprunt.date_retour is not None


class TestEmpruntServiceUnitaire:

    def test_creer_emprunt_unitaire(self, mocker):
        # Mocks des dépendances
        membre = mocker.Mock()
        membre.peut_emprunter.return_value = True

        media = mocker.Mock()
        media.est_disponible.return_value = True
        media.empruntable = True

        # Mock de l'appel ORM
        mock_create = mocker.patch(
            "administration.emprunt_service.Emprunt.objects.create",
            return_value=mocker.MagicMock(date_retour=None)
        )

        emprunt = creer_emprunt(membre, media)

        assert emprunt.date_retour is None
        mock_create.assert_called_once_with(
            membre=membre,
            media=media
        )
