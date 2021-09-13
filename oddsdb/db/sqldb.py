import logging
import os
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy import func, distinct
from sqlalchemy.orm import sessionmaker
from .. import models, locale

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
                  .group_by(oddsmodel.source, oddsmodel.match_date, oddsmodel.home_team, oddsmodel.away_team)
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
                      .group_by(oddsmodel.source, oddsmodel.match_date, oddsmodel.home_team, oddsmodel.away_team, oddsmodel.home, oddsmodel.away, oddsmodel.draw)
        if oddsmodel == models.Odds_Handicap:
            result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                      .group_by(oddsmodel.source, oddsmodel.match_date, oddsmodel.home_team, oddsmodel.away_team, oddsmodel.handicap, oddsmodel.home, oddsmodel.away)
        if oddsmodel in (models.Odds_HiLo, models.Odds_CornerHiLo):
            result = s.query(oddsmodel, func.count(distinct(oddsmodel.update_time)))\
                      .group_by(oddsmodel.source, oddsmodel.match_date, oddsmodel.home_team, oddsmodel.away_team, oddsmodel.line, oddsmodel.hi, oddsmodel.lo)
        if result:
            new_matches = self.get_new_matches(oddsmodel)
            new_matches = tuple((m.source, m.match_date, m.home_team, m.away_team) for m in new_matches)
            return tuple(r[0] for r in result if (r[1] == 1 and r[0].update_time == latest_update_time and (r[0].source, r[0].match_date, r[0].home_team, r[0].away_team) not in new_matches))

        return tuple()

    
    def notify_odds_change(self, change:str='new', notifier:callable=logging.info, oddstypes:Tuple[models.Odds]=(models.Odds_HomeDrawAway, models.Odds_Handicap, models.Odds_HiLo, models.Odds_CornerHiLo), lang:str='ch') -> None:
        
        if lang == 'ch':
            l = locale.ch
        elif lang == 'en':
            l = locale.en
        else:
            l = locale.ch

        if change.lower() == 'new':
            change_func = self.get_new_matches
            change_label = "新增賽事"
        elif change.lower() == 'update':
            change_func = self.get_updated_odds
            change_label = "賠率變動"
        else:
            return None

        for oddstype in oddstypes:
            oddstype_str = l['oddstype'][oddstype.__name__]
            changed_matches = change_func(oddstype)
        
            if not changed_matches: continue

            msg = f"{oddstype_str}{change_label}:\n"
            for m in changed_matches:
                msg += f"{m.match_date:%b-%d} {m.home_team} {l['vs']} {m.away_team} - "
                if oddstype == models.Odds_HomeDrawAway:
                    msg += f"主: {m.home} 客: {m.away} 和: {m.draw}"
                elif oddstype == models.Odds_Handicap:
                    msg += f"讓: {m.handicap} 主: {m.home} 客: {m.away}"
                elif oddstype in (models.Odds_HiLo, models.Odds_CornerHiLo):
                    msg += f"球: {m.line} 大: {m.hi} 細: {m.lo}"
                msg += "\n"
            
            notifier(msg)
        

class UnsupportedOddsModel(Exception):
    pass