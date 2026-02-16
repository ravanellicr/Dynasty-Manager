from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Fleet

router = APIRouter(prefix="/fleets", tags=["Fleets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_fleet(payload: dict, db: Session = Depends(get_db)):
    name = payload.get("name")

    if not name:
        raise HTTPException(status_code=400, detail="Fleet name is required")

    # Prevent duplicate fleet names
    existing = db.query(Fleet).filter(Fleet.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Fleet already exists")

    fleet = Fleet(name=name)

    db.add(fleet)
    db.commit()
    db.refresh(fleet)

    return {
        "id": fleet.id,
        "name": fleet.name
    }

@router.get("/")
def get_fleets(db: Session = Depends(get_db)):
    fleets = db.query(Fleet).all()

    return [
        {
            "id": fleet.id,
            "name": fleet.name,
            "ship_count": len(fleet.ships)
        }
        for fleet in fleets
    ]

@router.delete("/{fleet_id}")
def delete_fleet(fleet_id: int, db: Session = Depends(get_db)):
    fleet = db.query(Fleet).filter(Fleet.id == fleet_id).first()

    if not fleet:
        raise HTTPException(status_code=404, detail="Fleet not found")

    db.delete(fleet)
    db.commit()

    return {"status": "deleted"}
