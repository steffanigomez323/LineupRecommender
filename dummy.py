from updater import DailyUpdate
from projector import SimpleFeatureProjector
from db_helper import RedisHelper
from scorer import FanDuelScorer
from data_collector import NBAScraper
from data_collector import NBAStattleShip
from data_collector import NumberFireScraper

#import csv


u = DailyUpdate()
redis_db = RedisHelper()
redis_db.populate_db()
player_attr = u.nf_playerlookup()
#players_stats = u.get_feature_scores(players)
#sfp = SimpleFeatureProjector(players_stats)
#nf_scraper = 
#nf_scraper.get_todays_player_data()

#print player_attr

#layers = player_attr.keys()

#print len(player_attr)

nbascrape = NBAScraper()
#player_stats = nbascrape.get_player_stats('2015-16')
player_stats = nbascrape.get_player_stats('2014-15')
clean_player_stats = nbascrape.clean_player_stats2(player_stats)

nbastattle = NBAStattleShip()

#for p in players:
#	print p
print "###PLAYER STATS###"
print nbastattle.prepare_data_for_projections("nba-lebron-james")
print "###PLAYER STATS###\n"

print len(clean_player_stats)
print ""

for p in clean_player_stats:
	print p
	print clean_player_stats[p]
	print ""
	break

# with open("static/data/projection_visuals.csv", "wb") as viz:
# 	writer = csv.writer(viz)
# 	writer.writerow(["Player","Score","Points","Rebounds","Steals","Assists", "Turnovers", "Blocks", "Dates"])
# 	for p in players.keys():
# 		try:
# 			predicted = sfp.get_projection(p)
# 		except (ValueError, KeyError):
# 			continue
# 		else:
# 			for i in range(0, len(players_stats[p]["points"])):
# 				game = dict()
# 				game['3PT_FG'] = 0
# 				game['2PT_FG'] = 0
# 				game['FT'] = 0
# 				game['REB'] = players_stats[p]["rebounds"][i]
# 				game['AST'] = players_stats[p]["assists"][i]
# 				game['BLK'] = players_stats[p]["blocks"][i]
# 				game['STL'] = players_stats[p]["steals"][i]
# 				game['TOV'] = players_stats[p]["turnovers"][i]

# 				total_score = FanDuelScorer.find_fanduel_score(game)
# 				total_score += players_stats[p]["points"][i]
# 				writer.writerow([p, total_score, players_stats[p]["points"][i], players_stats[p]["rebounds"][i], players_stats[p]["steals"][i], players_stats[p]["assists"][i], players_stats[p]["turnovers"][i], players_stats[p]["blocks"][i], players_stats[p]["dates"][i]])
# 			writer.writerow([p, predicted["score"], predicted["points"], predicted["rebounds"], predicted["steals"], predicted["assists"], predicted["turnovers"], predicted["blocks"], "current"])
# from projector import SimpleFeatureProjector
# from db_helper import RedisHelper

# from data_collector import NBAStattleShip


# nss = NBAStattleShip()


# u = DailyUpdate()
# redis = RedisHelper()
# redis.populate_db()
# players = u.nf_playerlookup()
# players_stats = u.get_feature_scores(players)
# sfp = SimpleFeatureProjector(players_stats)

# for p in players.keys():

# 	print p, sfp.get_projection(p)

# ss.get_player_stats_data()

# rh = RedisHelper()
# rh.populate_db()

# nss.get_game_log_data('nba-steven-adams')
# nss.get_game_log_data('nba-jeff-adrien')

# nss.get_player_stats_data('nba-mitch-mcgary')
