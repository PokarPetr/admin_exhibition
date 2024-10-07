
from models.models import CatBreed
from .conftest import client, TestingSessionLocal

def test_add_breed(test_db):

    data = {
        "name": "Sphynx",
        "type": "Hairless",
        "description": "A breed of cat known for its lack of coat."
    }

    response = client.post("/add_breed", data=data)

    assert response.status_code == 200
    db = TestingSessionLocal()
    breed = db.query(CatBreed).filter(CatBreed.name == "Sphynx").first()
    assert breed is not None
    assert breed.type == "Hairless"
    assert breed.description == "A breed of cat known for its lack of coat."
    assert breed.is_active == True
    assert breed.create_time is not None
    assert breed.id is not None
    db.close()
