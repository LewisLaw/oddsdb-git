import configparser
from .db import sqldb
from .scraper import scraper
from . import locale
from . import models

def run(lang:str='ch', delay: int = 3, silence:bool=False):

    config = configparser.ConfigParser()
    config.read('./config.ini')  

    selenium_config = config['selenium_remote_container']
    #hkjc_scraper = scraper.HKJCScraper(selenium_config['Host'], selenium_config['Port'], lang, delay)

    #db_config = config['sql_db']
    #db_url=f"{db_config['Type']}://{db_config['User']}:{db_config['Pwd']}@{db_config['Host']}:{db_config['Port']}/{db_config['Db']}"
    #db = sqldb.SqlDB(url=db_url)
    db = sqldb.SqlDB()
    #scrapers = (hkjc_scraper.scrap_homedrawaway, )#hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    
    #matches = tuple()
    #for s in scrapers:
    #    matches += s()
    m0 = models.Match(
        datetime(2021, 9, 3, 13, 0),
        'NY Knickers',
        'SA Spurrs',
        [
            models.Odd_HomeAwayDraw('Lewis', datetime(2021, 9, 18, 8, 15), 95., 97., 93.),
        ]
    )
    m1 = models.Match(
        datetime(2021, 9, 3, 14, 0),
        'Suns',
        'Heats',
        [
            models.Odd_HomeAwayDraw('Lewis', datetime(2021, 9, 18, 8, 15), 8., 7., 3.),
        ]
    )
    m2 = models.Match(
        datetime(2021, 9, 3, 13, 0),
        'NY Knickers',
        'SA Spurrs',
        [
            models.Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '132', 99., 99.),
            models.Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '999', 12., 23.),
            models.Odd_HiLo('Lewis', datetime(2021, 9, 18, 8, 15), '88888888888', 43., 34.),
        ]
    )

    db.add_all((m0, m1, m2))
    #db.add_all(matches)
    
            #if odds:
        #    db.add_all(odds)

    '''
    if not silence:
        tgbot_logger = logging.getLogger('telegramBot')
        db.notify_odds_change('new', tgbot_logger.info)
        db.notify_odds_change('update', tgbot_logger.info)
    '''

import argparse
import logging
import logging.config
import time as timer
from datetime import datetime

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('-i', '--interval', type=int, default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('-d', '--delay', type=int, default=5, help=r"Seconds of delay on webscraping.")
parser.add_argument('-l', '--lang', type=str, default='ch', help=r"Language of webpage to parse.")
parser.add_argument('-s', '--silence', action='store_true', help=r"Silencing Telegram Bot notifications for Odds Changes.")
parser.add_argument('--debug', action='store_true', help=r"Log debug message.")
argv = parser.parse_args()

if __name__ == "__main__":
    
    logging.config.fileConfig(fname='./oddsdb/logger/logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    while True:
        logger.info(f"Start Running...")
        logger.debug(argv)
        try:
            run(argv.lang, argv.delay)
            logger.info("Run Successful!")
            if argv.interval <= 0: break
        except Exception as e:
            logger.error("Exception occurred", exc_info=True)
        finally:
            logger.info(f"Wait {argv.interval} mins for Next Run...")
            timer.sleep(argv.interval * 60)