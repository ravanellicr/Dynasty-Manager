from fastapi import APIRouter
from backend.database import SessionLocal
from backend.models import ShipComponent

router = APIRouter(prefix="/components", tags=["Components"])

@router.post("/")
def add_component(component: dict):
    db = SessionLocal()
    new_component = ShipComponent(**component)
    db.add(new_component)
    db.commit()
    db.refresh(new_component)
    return new_component

@router.get("/ship/{ship_id}")
def list_components(ship_id: int):
    db = SessionLocal()
    return db.query(ShipComponent).filter_by(ship_id=ship_id).all()
