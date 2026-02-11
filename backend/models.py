# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    homeworld = Column(String)
    career = Column(String)

class Fleet(Base):
    """
    Representa uma Frota pertencente a uma Dinastia.
    Uma frota pode ter múltiplos navios (voidships).
    
    Relacionamentos:
    - N:1 com Dynasty (várias frotas pertencem a uma dinastia)
    - 1:N com Voidship (uma frota tem vários navios)
    """
    __tablename__ = "fleets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)  # Descrição opcional da frota
    
    # Relacionamentos
    ships = relationship(
        "Voidship",
        back_populates="fleet",
        cascade="all, delete-orphan"
    )
    
class Voidship(Base):
    """
    Representa um Navio de Void (Voidship) em uma Frota.
    Armazena as estatísticas finais calculadas baseadas no casco e componentes.
    
    As estatísticas seguem as regras do sistema Rogue Trader
    
    Relacionamentos:
    - N:1 com Fleet (vários navios pertencem a uma frota)
    """
    __tablename__ = "voidships"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    hull_type = Column(String, nullable=False)  # Ex: "Armageddon", "Lunar", etc.
    fleet_id = Column(Integer, ForeignKey("fleets.id"), nullable=False)
    
    # Estatísticas finais do voidship (calculadas e persistidas)
    function_def =  Column(String, nullable=False)
    category = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    mass = Column(Integer, nullable=False)
    crew = Column(Integer, nullable=False)
    acceleration = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    detection = Column(Integer, nullable=False)
    maneuver = Column(Integer, nullable=False)
    hull_integrity = Column(Integer, nullable=False)
    armor = Column(Integer, nullable=False)
    turret = Column(Integer, nullable=False)
    space = Column(Integer, nullable=False)
    ship_point = Column(Integer, nullable=False)
    
    weapon_capacity_prow = Column(Integer, nullable=False)
    weapon_capacity_port = Column(Integer, nullable=False)
    weapon_capacity_starboard = Column(Integer, nullable=False)
    weapon_capacity_dorsal = Column(Integer, nullable=False)
    weapon_capacity_keel = Column(Integer, nullable=False)
    
    endeavours_military = Column(Integer, nullable=False)
    endeavours_criminal = Column(Integer, nullable=False)
    endeavours_exploration = Column(Integer, nullable=False)
    endeavours_trade = Column(Integer, nullable=False)
    endeavours_creed = Column(Integer, nullable=False)

    special = Column(String, nullable=False)

    # Relacionamento
    fleet = relationship("Fleet", back_populates="ships")
    