import pytest
from server import loadClubs, loadCompetitions, app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'something_special'
    app.clubs = loadClubs()
    app.competitions = loadCompetitions()

    client = app.test_client()
    return client


def test_purchasePlaces(client):
    """Test pour vérifier si un club peut booker des places dans une compétition existante"""
    data = {
        "competition": "Fall Classic",
        "club": "She Lifts",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 200

    # TEST OK


def test_purchasePlaces_invalid_competition(client):
    """Test pour vérifier si un club peut booker des places dans une compétition inexistante"""
    data = {
        "competition": "InvalidCompetitionName",
        "club": "Simply Lift",
        "places": "1",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 404  # 404 : Ressource non trouvée

    # LE RETOUR ACTUEL EST " INTERNAL SERVER ERROR" / IndexError : list index out of range pour competition['name']


def test_purchasePlaces_invalid_club(client):
    """Test pour vérifier si un club inexsitant peut booker des places dans une compétition existante"""

    data = {
        "competition": "Spring Festival",
        "club": "InvalidClubName",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 404  # 404 : Ressource non trouvée

    # LE RETOUR ACTUEL EST " INTERNAL SERVER ERROR" / IndexError : list index out of range pour club['email']


def test_purchasePlaces_not_enough_points(client):
    """Test pour vérifier si un club peut booker plus de places qu'il a de point"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "12",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 403  # 403 : Accès refusé

    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"


def test_purchasePlaces_negative_places(client):
    """Test pour vérifier si un club peut booker un nombre de place négatif"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "-3",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 403  # 403 : Accès refusé

    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"


def test_purchasePlaces_max_places_exceeded(client):
    """Test pour vérifier si un club peut booker un nombre de place > nombre de points disponible"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "15",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 403

    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"


def test_purchasePlaces_no_places_specified(client):
    """Test pour vérifier si un club peut booker un nombre de place =0"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "0",
    }
    response_no_places = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response_no_places.status_code == 400

    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"


def test_purchasePlaces_too_many_places(client):
    """Test pour vérifier si un club peut booker un nombre de place >12"""
    data_too_many_places = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "30",
    }
    response_too_many_places = client.post(
        "/purchasePlaces", data=data_too_many_places
    )
    assert response_too_many_places.status_code == 403

    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"