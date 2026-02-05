from fastapi import APIRouter
from backend.database import SessionLocal
from backend.models import Character

router = APIRouter(prefix="/characters", tags=["Characters"])

@router.post("/")
def create_character(character: dict):
    db = SessionLocal()
    new_char = Character(**character)
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

@router.get("/")
def list_characters():
    db = SessionLocal()
    return db.query(Character).all()
