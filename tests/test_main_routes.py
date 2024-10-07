# tests/test_app.py
from .conftest import client


def test_home_route():
    response = client.get("/")

    assert response.status_code == 200
    assert b'home' in response.content
    assert b'breeds' in response.content
    assert b'kittens' in response.content

def test_breeds(test_db, create_breeds):
    response = client.get("/breeds")

    assert response.status_code == 200
    assert "Siamese" in response.text
    assert 'Cats' in response.text
    assert "Elegant and vocal cats." in response.text
    assert "Persian" in response.text
    assert "Long-haired and gentle cats." in response.text


def test_kittens(test_db, create_kittens):
    response = client.get("/kittens")

    assert "KIT001" in response.text
    assert "Luffy" in response.text
    assert "Black" in response.text
    assert "7" in response.text
    assert "Siamese" in response.text

    assert "KIT002" in response.text
    assert "Mixen" in response.text
    assert "Ginger" in response.text
    assert "9" in response.text
    assert "Persian" in response.text


