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
def create_fleet(dynasty_id: int, db: Session = Depends(get_db)):
    fleet = models.Fleet(dynasty_id=dynasty_id)

    db.add(fleet)
    db.commit()
    db.refresh(fleet)

    return fleet


@router.get("/dynasty/{dynasty_id}")
def get_dynasty_fleet(dynasty_id: int, db: Session = Depends(get_db)):
    return db.query(models.Fleet).filter(models.Fleet.dynasty_id == dynasty_id).all()


@router.delete("/{fleet_id}")
def delete_fleet(fleet_id: int, db: Session = Depends(get_db)):
    fleet = db.query(models.Fleet).get(fleet_id)

    if not fleet:
        raise HTTPException(status_code=404, detail="Fleet not found")

    db.delete(fleet)
    db.commit()

    return {"detail": "Fleet deleted"}
