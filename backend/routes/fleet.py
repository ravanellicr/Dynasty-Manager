from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_ship(dynasty_id: int, name: str, db: Session = Depends(get_db)):
    ship = models.Ship(name=name, dynasty_id=dynasty_id)

    db.add(ship)
    db.commit()
    db.refresh(ship)

    return ship


@router.get("/dynasty/{dynasty_id}")
def get_dynasty_ships(dynasty_id: int, db: Session = Depends(get_db)):
    return db.query(models.Ship).filter(models.Ship.dynasty_id == dynasty_id).all()


@router.delete("/{ship_id}")
def delete_ship(ship_id: int, db: Session = Depends(get_db)):
    ship = db.query(models.Ship).get(ship_id)

    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")

    db.delete(ship)
    db.commit()

    return {"detail": "Ship deleted"}
