from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

nba = NBAScraper()
# print nba_players


# stattleship = NBAStattleShip()
# stattleship_data = stattleship.get_player_data()
# stattleship_players = stattleship.get_player_fields(stattleship_data)
# print stattleship_players

# nf_player_set = set()
# nf = NumberFireScraper()
# nf_players = nf.get_all_player_data() # will print the names
# for nf_player in nf_players:
# 	nf_player_set.add(nf_player)

# print nf_player_set
# print "#########"

# print len(nf_player_set - nba_player_set) # nf_players not in nba list

nba_players = nba.get_player_data()
nba_name_to_id = nba.get_player_name_id_map(nba_players)
nba_names = set([])

for nba_name, nba_id in nba_name_to_id.iteritems():
    nba_names.add(nba_name)

print len(nba_name_to_id)

stattleship = NBAStattleShip()
stattleship_players = stattleship.get_player_data()
stattleship_name_to_slug = stattleship.get_player_name_slug_map(stattleship_players)
stattleship_names = set([])

for stattleship_name, stattleship_slug in stattleship_name_to_slug.iteritems():
    stattleship_names.add(stattleship_name)

for name in nba_names:
    nba_id = nba_name_to_id[name]
    stattleship_slug = stattleship_name_to_slug[name]
    redis_db.set(nba_id, stattleship_slug)




