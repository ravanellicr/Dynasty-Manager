from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json

from backend.routes import dynasties, characters, fleets, voidship

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("dynasties", exist_ok=True)

# Include your API routers
app.include_router(dynasties.router)
app.include_router(characters.router)
app.include_router(fleets.router)
app.include_router(voidship.router)

# API Endpoints
@app.get("/api/hulls")
def get_hulls():
    with open("backend/data/hulls.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Serve static files (CSS, JS, images) - MUST be after routers
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve HTML pages
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")  # Change to your main page name

@app.get("/dashboard")
def dashboard_page():
    return FileResponse("frontend/dashboard.html")

@app.get("/characters")
def characters_page():
    return FileResponse("frontend/characters.html")

@app.get("/fleets")
def fleets_page():
    return FileResponse("frontend/fleets.html")

@app.get("/voidships")
def voidships_page():
    return FileResponse("frontend/voidships.html")

@app.get("/voidship_details")
def voidship_details_page():
    return FileResponse("frontend/voidship_details.html")