from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

nba = NBAScraper()
# print nba_players

player_stats = nba.get_player_stats()
projection_data = nba.prepare_data_for_projections(player_stats)

for p in projection_data:
	print "### PLAYER ###"
	print p
	print projection_data[p]['allgames']
	print ""