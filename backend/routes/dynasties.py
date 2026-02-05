import os
import shutil
from fastapi import APIRouter

import backend.database as db
from backend.database import Base
from backend import models


router = APIRouter(prefix="/dynasties", tags=["Dynasties"])

DYNASTY_FOLDER = "dynasties"

@router.get("/")
def list_dynasties():
    return [f.replace(".db", "") for f in os.listdir(DYNASTY_FOLDER) if f.endswith(".db")]

@router.post("/create/{name}")
def create_dynasty(name: str):
    path = os.path.join(DYNASTY_FOLDER, f"{name}.db")
    open(path, "a").close()
    return {"status": "created"}

@router.post("/copy/{name}")
def copy_dynasty(name: str):
    src = os.path.join(DYNASTY_FOLDER, f"{name}.db")
    dst = os.path.join(DYNASTY_FOLDER, f"{name}_copy.db")
    shutil.copy(src, dst)
    return {"status": "copied"}

@router.delete("/delete/{name}")
def delete_dynasty(name: str):
    os.remove(os.path.join(DYNASTY_FOLDER, f"{name}.db"))
    return {"status": "deleted"}

@router.post("/activate/{name}")
def activate_dynasty(name: str):
    db_path = os.path.join(DYNASTY_FOLDER, f"{name}.db")

    # Switch active database
    db.set_database(db_path)

    # Create tables inside the selected dynasty file
    Base.metadata.create_all(bind=db.engine)

    return {"status": "activated"}

