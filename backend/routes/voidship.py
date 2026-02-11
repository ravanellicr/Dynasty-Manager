from fastapi import APIRouter, HTTPException
from backend.data.hulls import HULL_TEMPLATES

router = APIRouter()

@router.get("/hulls")
def list_hulls():
    return list(HULL_TEMPLATES.keys())


@router.get("/hulls/{hull_name}")
def get_hull(hull_name: str):
    hull = HULL_TEMPLATES.get(hull_name)
    if not hull:
        raise HTTPException(status_code=404, detail="Hull not found")
    return hull
