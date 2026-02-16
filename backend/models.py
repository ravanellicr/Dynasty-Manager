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
    
    # REQUIRED FIELDS ONLY
    id = Column(Integer, primary_key=True, index=True)
    fleet_id = Column(Integer, ForeignKey("fleets.id"), nullable=False)
    
    # ALL OTHER FIELDS SHOULD BE NULLABLE OR HAVE DEFAULTS
    name = Column(String, nullable=True, default="Unnamed Voidship", index=True)  
    hull_type = Column(String, nullable=True)  
    
    # Estatísticas finais do voidship (calculadas e persistidas)
    function_def = Column(String, nullable=True)  
    category = Column(String, nullable=True)  
    length = Column(Integer, nullable=True, default=0)  
    width = Column(Integer, nullable=True, default=0)  
    mass = Column(Integer, nullable=True, default=0)  
    crew = Column(Integer, nullable=True, default=0)  
    acceleration = Column(Integer, nullable=True, default=0)  
    speed = Column(Integer, nullable=True, default=0)  
    detection = Column(Integer, nullable=True, default=0)  
    maneuver = Column(Integer, nullable=True, default=0)  
    hull_integrity = Column(Integer, nullable=True, default=0)  
    armor = Column(Integer, nullable=True, default=0)  
    turret = Column(Integer, nullable=True, default=0)  
    space = Column(Integer, nullable=True, default=0)  
    ship_point = Column(Integer, nullable=True, default=0)  
    
    weapon_capacity_prow = Column(Integer, nullable=True, default=0)  
    weapon_capacity_port = Column(Integer, nullable=True, default=0)  
    weapon_capacity_starboard = Column(Integer, nullable=True, default=0)  
    weapon_capacity_dorsal = Column(Integer, nullable=True, default=0)  
    weapon_capacity_keel = Column(Integer, nullable=True, default=0)  
    
    endeavours_military = Column(Integer, nullable=True, default=0)  
    endeavours_criminal = Column(Integer, nullable=True, default=0)  
    endeavours_exploration = Column(Integer, nullable=True, default=0)  
    endeavours_trade = Column(Integer, nullable=True, default=0)  
    endeavours_creed = Column(Integer, nullable=True, default=0)  

    special = Column(String, nullable=True)  

    """
      Aqui a ideia é usar codigos id de duas partes como string para 
      salvar os equipamento, por exemplo drive vai ser 1_4, 
      1 > Id do drive 4 > Modificador simbolizando Best Quality
    """

    essential_plasma_drive = Column(String, nullable=True)  
    essential_warp_drive = Column(String, nullable=True)  
    essential_gellar_field = Column(String, nullable=True)  
    essential_void_shield = Column(String, nullable=True)  
    essential_ship_bridge = Column(String, nullable=True)  
    essential_life_sustainer = Column(String, nullable=True)  
    essential_crew_quarters = Column(String, nullable=True)  
    essential_augur_array = Column(String, nullable=True)  

    suplemental_components = Column(String, nullable=True)  

    # Relacionamento
    fleet = relationship("Fleet", back_populates="ships")
    