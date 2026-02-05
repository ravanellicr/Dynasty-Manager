# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
SessionLocal = sessionmaker()
engine = None  # This will change when a dynasty is loaded

def set_database(db_path: str):
    global engine
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False}
    )
    SessionLocal.configure(bind=engine)
