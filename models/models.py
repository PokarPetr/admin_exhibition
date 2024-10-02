#models/models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Breed(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False) # Cat or Dog
    description = Column(String, nullable=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Breed(name={self.name}, type={self.type}, active={self.is_active})>"

class CatBreed(Breed):
    __tablename__ = "cat_breed"
    kittens = relationship("Kitten", back_populates="breed")

class Animal(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    age_months = Column(Integer, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Animal(name={self.name}, nickname={self.nickname}, active={self.is_active})>"

class Kitten(Animal):
    __tablename__ = "kitten"
    breed_id = Column(Integer, ForeignKey('cat_breed.id'))
    breed = relationship("CatBreed", back_populates="kittens")

# class DogBreed(Breed):
#     __tablename__ = "dog-breed"
