from dataclasses import dataclass, field
from sqlalchemy import create_engine, Column, String, Date, DateTime, Float
from sqlalchemy.orm import registry
import datetime

mapper_registry = registry()
Base = mapper_registry.generate_base()

@dataclass
class Odds():
    source: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    match_date: datetime.date = field(
        metadata={
            'sa': Column(Date, primary_key=True)
        }
    )
    home_team: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    away_team: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )
    cutoff_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )

@mapper_registry.mapped
@dataclass
class Odds_HomeDrawAway(Odds):
    __tablename__ = "Odds_HomeDrawAway"
    __sa_dataclass_metadata_key__ = "sa"
    source: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    match_date: datetime.date = field(
        metadata={
            'sa': Column(Date, primary_key=True)
        }
    )
    home_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    away_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    cutoff_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )
    home: float = field(
        metadata={
            'sa': Column(Float)
        }
    )
    away: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    draw: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@mapper_registry.mapped
@dataclass
class Odds_Handicap(Odds):
    __tablename__ = "Odds_Handicap"
    __sa_dataclass_metadata_key__ = "sa"
    source: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    match_date: datetime.date = field(
        metadata={
            'sa': Column(Date, primary_key=True)
        }
    )
    home_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    away_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    handicap: str= field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    cutoff_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )
    home: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    away: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@mapper_registry.mapped
@dataclass
class Odds_HiLo(Odds):
    __tablename__ = "Odds_HiLo"
    __sa_dataclass_metadata_key__ = "sa"
    source: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    match_date: datetime.date = field(
        metadata={
            'sa': Column(Date, primary_key=True)
        }
    )
    home_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    away_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    line: str= field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    cutoff_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )
    hi: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    lo: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@mapper_registry.mapped
@dataclass
class Odds_CornerHiLo(Odds):
    __tablename__ = "Odds_CornerHiLo"
    __sa_dataclass_metadata_key__ = "sa"
    source: str = field(
        metadata={
            'sa': Column(String(256))
        }
    )
    match_date: datetime.date = field(
        metadata={
            'sa': Column(Date, primary_key=True)
        }
    )
    home_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    away_team: str = field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    line: str= field(
        metadata={
            'sa': Column(String(256), primary_key=True)
        }
    )
    cutoff_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )
    hi: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    lo: float= field(
        metadata={
            'sa': Column(Float)
        }
    )