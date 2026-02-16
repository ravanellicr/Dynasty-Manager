from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Voidship

router = APIRouter(prefix="/ships", tags=["Ships"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_ship(payload: dict, db: Session = Depends(get_db)):
    """Create a minimal ship with only fleet_id"""
    fleet_id = payload.get("fleet_id")

    if not fleet_id:
        raise HTTPException(status_code=400, detail="fleet_id is required")

    # Create minimal ship entry
    ship = Voidship(
        fleet_id=fleet_id,
        name=payload.get("name", "Unnamed Voidship")  # Optional name
    )

    db.add(ship)
    db.commit()
    db.refresh(ship)

    return {
        "id": ship.id,
        "fleet_id": ship.fleet_id,
        "name": ship.name
    }


@router.get("/fleet/{fleet_id}")
def get_ships_by_fleet(fleet_id: int, db: Session = Depends(get_db)):
    """Get all ships for a specific fleet"""
    ships = db.query(Voidship).filter(Voidship.fleet_id == fleet_id).all()

    return [
        {
            "id": ship.id,
            "fleet_id": ship.fleet_id,
            "name": ship.name,
        }
        for ship in ships
    ]


@router.get("/{ship_id}")
def get_ship(ship_id: int, db: Session = Depends(get_db)):
    """Get a single ship by ID"""
    ship = db.query(Voidship).filter(Voidship.id == ship_id).first()

    if not ship:
        raise HTTPException(status_code=404, detail="Voidship not found")

    return {
        "id": ship.id,
        "fleet_id": ship.fleet_id,
        "name": ship.name,
        "hull_type": ship.hull_type,
        # Add other fields as needed
    }


@router.post("/{ship_id}/copy")
def copy_ship(ship_id: int, db: Session = Depends(get_db)):
    """Create a copy of an existing ship"""
    original = db.query(Voidship).filter(Voidship.id == ship_id).first()

    if not original:
        raise HTTPException(status_code=404, detail="Voidship not found")

    # Create copy with all attributes
    copied_ship = Voidship(
        fleet_id=original.fleet_id,
        name=f"{original.name} (Copy)",
        hull_type=original.hull_type,
        function_def=original.function_def,
        category=original.category,
        length=original.length,
        width=original.width,
        mass=original.mass,
        crew=original.crew,
        acceleration=original.acceleration,
        speed=original.speed,
        detection=original.detection,
        maneuver=original.maneuver,
        hull_integrity=original.hull_integrity,
        armor=original.armor,
        turret=original.turret,
        space=original.space,
        ship_point=original.ship_point,

        weapon_capacity_prow=original.weapon_capacity_prow,
        weapon_capacity_port=original.weapon_capacity_port,
        weapon_capacity_starboard=original.weapon_capacity_starboard,
        weapon_capacity_dorsal=original.weapon_capacity_dorsal,
        weapon_capacity_keel=original.weapon_capacity_keel,

        endeavours_military=original.endeavours_military,
        endeavours_criminal=original.endeavours_criminal,
        endeavours_exploration=original.endeavours_exploration,
        endeavours_trade=original.endeavours_trade,
        endeavours_creed=original.endeavours_creed,

        special=original.special,

        essential_plasma_drive=original.essential_plasma_drive,
        essential_warp_drive=original.essential_warp_drive,
        essential_gellar_field=original.essential_gellar_field,
        essential_void_shield=original.essential_void_shield,
        essential_ship_bridge=original.essential_ship_bridge,
        essential_life_sustainer=original.essential_life_sustainer,
        essential_crew_quarters=original.essential_crew_quarters,
        essential_augur_array=original.essential_augur_array,
        
        suplemental_components=original.suplemental_components,
    )

    db.add(copied_ship)
    db.commit()
    db.refresh(copied_ship)

    return {
        "id": copied_ship.id,
        "fleet_id": copied_ship.fleet_id,
        "name": copied_ship.name
    }


@router.delete("/{ship_id}")
def delete_ship(ship_id: int, db: Session = Depends(get_db)):
    """Delete a ship"""
    ship = db.query(Voidship).filter(Voidship.id == ship_id).first()

    if not ship:
        raise HTTPException(status_code=404, detail="Voidship not found")

    db.delete(ship)
    db.commit()

    return {"status": "deleted", "id": ship_id}