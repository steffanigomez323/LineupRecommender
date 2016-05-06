from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

nf_name_set = set([])
nba_player_set = set([])

nf_scraper = NumberFireScraper()
nba_scraper = NBAScraper()

nf_name_to_slug = nf_scraper.get_player_name_slug_map()

nba_players = nba_scraper.get_player_data()
nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

for nf_name, nf_slug in nf_name_to_slug.iteritems():
    nf_name_set.add(nf_name)

for nba_name, nba_id in nba_name_to_id.iteritems():    
    nba_player_set.add(nba_name)

nba_players = nba_scraper.get_player_data()
nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

print "NF NAME SET"
print nf_name_to_slug
print "NBA NAME SET"
print nba_name_to_id
print "MISMATCHES"
print nf_name_set - nba_player_set