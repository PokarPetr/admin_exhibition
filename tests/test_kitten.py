#tets/test_add_kitten.py
from models.models import Kitten
from .conftest import client, TestingSessionLocal

def test_add_kitten(test_db):
    with TestingSessionLocal() as db:
        data = {
            "nickname": "TestKit",
            "name": "Sphynx",
            "color": "SilverBlack",
            "age_months": 6,
            "description": "A kitten of brilliant",
            'breed_id': 1
        }

        response = client.post("/add_kitten", data=data)

        assert response.status_code == 200
        kitten = db.query(Kitten).filter(Kitten.name == "Sphynx").first()
        assert kitten is not None
        assert kitten.nickname == "TestKit"
        assert kitten.color == "SilverBlack"
        assert kitten.age_months == 6
        assert kitten.description == "A kitten of brilliant"
        assert kitten.breed_id == 1
        assert kitten.is_active == True
        assert kitten.create_time is not None
        assert kitten.id is not None


def test_update_kitten(test_db, create_kittens):
    kitten1, kitten2 = create_kittens
    kitten_id = kitten1.id
    with TestingSessionLocal() as db:
        data_update = {
            "kitten_id": kitten_id,
            "name": "UpdateSphynx",
            "color": "UpdatedColor",
            "age_months": 7,
            "description": "Updated description",
            'breed_id': 1
        }

        response_update = client.post(f"/update_kitten/{kitten_id}", data=data_update)

        assert response_update.status_code == 200
        db.expire_all()
        updated_kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
        assert updated_kitten.nickname is not None
        assert updated_kitten.name == "UpdateSphynx"
        assert updated_kitten.color == "UpdatedColor"
        assert updated_kitten.age_months == 7
        assert updated_kitten.description == "Updated description"

def test_delete_kitten(test_db, create_kittens):
    with TestingSessionLocal() as db:
        kitten1, kitten2 = create_kittens
        kitten_id = kitten1.id

        response = client.post(f"/delete_kitten/{kitten_id}")
        assert response.status_code == 200
        db.expire_all()
        deleted_kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
        assert deleted_kitten.is_active == False
