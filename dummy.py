from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

nba = NBAScraper()
nba_players = nba.clean_players(nba.get_players())
# print nba_players

nba_player_set = set()
for nba_player in nba_players:
	nba_player_set.add(nba_player)

print nba_player_set

print "#######"

# stattleship = NBAStattleShip()
# stattleship_data = stattleship.get_player_data()
# stattleship_players = stattleship.get_player_fields(stattleship_data)
# print stattleship_players

nf_player_set = set()
nf = NumberFireScraper()
nf_players = nf.get_all_player_data() # will print the names
for nf_player in nf_players:
	nf_player_set.add(nf_player)

print nf_player_set
print "#########"

print len(nf_player_set - nba_player_set) # nf_players not in nba list


