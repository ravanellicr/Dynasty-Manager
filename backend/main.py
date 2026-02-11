from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.routes import dynasties, characters, fleets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("dynasties", exist_ok=True)

app.include_router(dynasties.router)
app.include_router(characters.router)
app.include_router(fleets.router)