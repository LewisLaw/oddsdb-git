import os
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy import func, distinct
from sqlalchemy.orm import sessionmaker
from .. import models

class SqlDB:
    def __init__(self, url:str='sqlite:///oddsdb.sqlite') -> None:
        self.engine = create_engine(url)
        models.Base.metadata.create_all(self.engine)
        self.sessionfactory = sessionmaker(bind=self.engine)
    
    def add_all(self, odds:Tuple[models.Odds]) -> None:
        s = self.sessionfactory()
        s.add_all(odds)
        s.commit()

        
    def get_new_matches(self, oddsmodel:models.Odds = models.Odds_HomeDrawAway) -> Tuple:
        s = self.sessionfactory()
        if oddsmodel not in (models.Odds_HomeDrawAway, models.Odds_Handicap, models.Odds_HiLo, models.Odds_CornerHiLo):
            raise UnsupportedOddsModel
        latest_update_time = s.query(func.max(oddsmodel.update_time)).scalar()
        result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                  .group_by(oddsmodel.source, oddsmodel.date, oddsmodel.teams)
        if result:
            return tuple(r[0] for r in result if (r[1] == 1 and r[0].update_time == latest_update_time))
        return tuple()

    
    def get_updated_odds(self, oddsmodel:models.Odds = models.Odds_HomeDrawAway) -> Tuple:
        s = self.sessionfactory()
        if oddsmodel not in (models.Odds_HomeDrawAway, models.Odds_Handicap, models.Odds_HiLo, models.Odds_CornerHiLo):
            raise UnsupportedOddsModel
        latest_update_time = s.query(func.max(oddsmodel.update_time)).scalar()
        if oddsmodel == models.Odds_HomeDrawAway:
            result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                      .group_by(oddsmodel.source, oddsmodel.date, oddsmodel.teams, oddsmodel.home, oddsmodel.away, oddsmodel.draw)
        if oddsmodel == models.Odds_Handicap:
            result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                      .group_by(oddsmodel.source, oddsmodel.date, oddsmodel.teams, oddsmodel.handicap, oddsmodel.home, oddsmodel.away)
        if oddsmodel in (models.Odds_HiLo, models.Odds_CornerHiLo):
            result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                      .group_by(oddsmodel.source, oddsmodel.date, oddsmodel.teams, oddsmodel.line, oddsmodel.hi, oddsmodel.lo)
        if result:
            new_matches = self.get_new_matches(oddsmodel)
            new_matches = tuple((m.source, m.date, m.teams) for m in new_matches)
            return tuple(r[0] for r in result if (r[1] == 1 and r[0].update_time == latest_update_time and (r[0].source, r[0].date, r[0].teams) not in new_matches))

        return tuple()


class UnsupportedOddsModel(Exception):
    pass

if __name__ == '__main__':
    db = SqliteDB()
    new_odds = db.get_updated_odds(models.Odds_HiLo)
    print(new_odds)