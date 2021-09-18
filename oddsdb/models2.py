from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from sqlalchemy.sql.sqltypes import Float

mapper_registry = registry()
Base = mapper_registry.generate_base()

@mapper_registry.mapped
@dataclass
class Match:
    __tablename__ = "match"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, 
        metadata={'sa': Column(Integer, primary_key=True, autoincrement=True)}
    )

    start_time: datetime = field(
        metadata={'sa': Column(DateTime)}
    )

    home_team: str = field(
        metadata={'sa': Column(String(50))}
    )

    away_team: str = field(
        metadata={'sa': Column(String(50))}
    )

    odds: List = field(
        default_factory=list, metadata={"sa": relationship("Odd", backref="match")}
    )

@mapper_registry.mapped
@dataclass
class Odd:  
    __tablename__ = "odd"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, 
        metadata={'sa': Column(Integer, primary_key=True, autoincrement=True)}
    )

    match_id: int = field(
        init=False, 
        metadata={'sa': Column(ForeignKey("match.id"))}
    )

    source: str = field(
        metadata={'sa': Column(String(50))}
    )

    update_time: datetime = field(
        metadata={'sa': Column(DateTime)}
    )

    type: str = field(
        init=False,
        metadata={'sa': Column(String(50))}
    )

    __mapper_args__ = {
        "polymorphic_identity": "odd",
        "polymorphic_on": "type",
    }

@mapper_registry.mapped
@dataclass
class Odd_HomeAwayDraw(Odd):
    __tablename__ = "odd_homeawydraw"
    __sa_dataclass_metadata_key__ = "sa"
    
    id: int = field(
        init=False, 
        metadata={'sa': Column(ForeignKey("odd.id"), primary_key=True)}
    )

    home: float = field(
        metadata={'sa': Column(Float)}
    )
    away: float = field(
        metadata={'sa': Column(Float)}
    )
    draw: float = field(
        metadata={'sa': Column(Float)}
    )

    __mapper_args__ = {
        "polymorphic_identity": "odd_homeawaydraw",
    }

@mapper_registry.mapped
@dataclass
class Odd_Handicap(Odd):
    __tablename__ = "odd_handicap"
    __sa_dataclass_metadata_key__ = "sa"
    
    id: int = field(
        init=False, 
        metadata={'sa': Column(ForeignKey("odd.id"), primary_key=True)}
    )

    handicap: str = field(
        metadata={'sa': Column(String(50))}
    )

    home: float = field(
        metadata={'sa': Column(Float)}
    )
    away: float = field(
        metadata={'sa': Column(Float)}
    )

    __mapper_args__ = {
        "polymorphic_identity": "odd_handicap",
    }

@mapper_registry.mapped
@dataclass
class Odd_HiLo(Odd):
    __tablename__ = "odd_hilo"
    __sa_dataclass_metadata_key__ = "sa"
    
    id: int = field(
        init=False, 
        metadata={'sa': Column(ForeignKey("odd.id"), primary_key=True)}
    )

    line: str = field(
        metadata={'sa': Column(String(50))}
    )

    hi: float = field(
        metadata={'sa': Column(Float)}
    )
    lo: float = field(
        metadata={'sa': Column(Float)}
    )

    __mapper_args__ = {
        "polymorphic_identity": "odd_hilo",
    }

@mapper_registry.mapped
@dataclass
class Odd_CornerHiLo(Odd):
    __tablename__ = "odd_cornerhilo"
    __sa_dataclass_metadata_key__ = "sa"
    
    id: int = field(
        init=False, 
        metadata={'sa': Column(ForeignKey("odd.id"), primary_key=True)}
    )

    line: str = field(
        metadata={'sa': Column(String(50))}
    )

    hi: float = field(
        metadata={'sa': Column(Float)}
    )
    lo: float = field(
        metadata={'sa': Column(Float)}
    )

    __mapper_args__ = {
        "polymorphic_identity": "odd_cornerhilo",
    }




import os
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')  

db_config = config['sql_db']
db_url=f"{db_config['Type']}://{db_config['User']}:{db_config['Pwd']}@{db_config['Host']}:{db_config['Port']}/{db_config['Db']}"

absp = os.path.abspath("./oddsdb.sqlite")
#engine = create_engine(f"sqlite:///{absp}", echo=True)9
engine = create_engine(db_url, echo=True)
Base.metadata.create_all(engine)

session = Session(engine)


m = Match(
    datetime(2021, 9, 3, 13, 0),
    'NY Knickers',
    'SA Spurrs',
    [
        Odd_HomeAwayDraw('Lewis', datetime(2021, 9, 18, 8, 15), 95., 97., 93.),
        Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '132', 99., 99.),
        Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '2>3', 12., 23.),
        Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '3>4', 43., 34.),
    ]
)



session.add(m)
session.commit()
