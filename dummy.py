from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

nba = NBAScraper()
nba_players = nba.clean_players(nba.get_players())

stattleship = NBAStattleShip()
stattleship_data = stattleship.get_player_data()
stattleship_players = stattleship.get_player_fields(stattleship_data)
print stattleship_players
