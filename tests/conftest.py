#tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models.models import CatBreed, Kitten
from utils.db import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        app.dependency_overrides[get_db] = lambda: db
        yield db
    finally:
        app.dependency_overrides[get_db] = get_db
        db.close()

@pytest.fixture
def create_breeds(test_db):
    breed1 = test_db.query(CatBreed).filter_by(name="Siamese").first()
    breed2 = test_db.query(CatBreed).filter_by(name="Persian").first()

    if not breed1:
        breed1 = CatBreed(name="Siamese", type="Cats", description="Elegant and vocal cats.")
        test_db.add(breed1)

    if not breed2:
        breed2 = CatBreed(name="Persian", type="Cats", description="Long-haired and gentle cats.")
        test_db.add(breed2)

    test_db.commit()
    return breed1, breed2

@pytest.fixture
def create_kittens(test_db, create_breeds):
    breed1, breed2 = create_breeds
    kitten1 = test_db.query(Kitten).filter_by(nickname="KIT001").first()
    kitten2 = test_db.query(Kitten).filter_by(nickname="KIT002").first()
    if not kitten1:
        kitten1 = Kitten(nickname="KIT001", name="Luffy", color="Black", age_months=7,
                         description="Tuff kitten", breed_id=breed1.id)
        test_db.add(kitten1)
    if not kitten2:
        kitten2 = Kitten(nickname="KIT002", name="Mixen", color="Ginger", age_months=9,
                         description="Nice kitten", breed_id=breed2.id)
        test_db.add(kitten2)

    test_db.commit()
    return kitten1, kitten2

