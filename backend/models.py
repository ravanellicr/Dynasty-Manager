# backend/models.py
from sqlalchemy import Column, Integer, String
from backend.database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    homeworld = Column(String)
    career = Column(String)

class Ship(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hull_type = Column(String, default="Unassigned")
    hull_integrity = Column(Integer)
