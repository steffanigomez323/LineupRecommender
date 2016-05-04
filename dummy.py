from updater import DailyUpdate
from projector import SimpleFeatureProjector

from db_helper import RedisHelper
from scorer import FanDuelScorer

import csv


u = DailyUpdate()
redis_db = RedisHelper()
redis_db.populate_db()
players = u.nf_playerlookup()
players_stats = u.get_feature_scores(players)
sfp = SimpleFeatureProjector(players_stats)

with open("static/data/projection_visuals.csv", "wb") as viz:
	writer = csv.writer(viz)
	writer.writerow(["Player","Score","Points","Rebounds","Steals","Assists", "Turnovers", "Blocks", "Dates"])
	for p in players.keys():
		try:
			predicted = sfp.get_projection(p)
		except (ValueError, KeyError):
			continue
		else:
			for i in range(0, len(players_stats[p]["points"])):
				game = dict()
				game['3PT_FG'] = 0
				game['2PT_FG'] = 0
				game['FT'] = 0
				game['REB'] = players_stats[p]["rebounds"][i]
				game['AST'] = players_stats[p]["assists"][i]
				game['BLK'] = players_stats[p]["blocks"][i]
				game['STL'] = players_stats[p]["steals"][i]
				game['TOV'] = players_stats[p]["turnovers"][i]

				total_score = FanDuelScorer.find_fanduel_score(game)
				total_score += players_stats[p]["points"][i]
				writer.writerow([p, total_score, players_stats[p]["points"][i], players_stats[p]["rebounds"][i], players_stats[p]["steals"][i], players_stats[p]["assists"][i], players_stats[p]["turnovers"][i], players_stats[p]["blocks"][i], players_stats[p]["dates"][i]])
			writer.writerow([p, predicted["score"], predicted["points"], predicted["rebounds"], predicted["steals"], predicted["assists"], predicted["turnovers"], predicted["blocks"], "current"])