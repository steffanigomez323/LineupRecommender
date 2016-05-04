from updater import DailyUpdate
# from projector import SimpleFeatureProjector
from db_helper import RedisHelper


# u = DailyUpdate()
# redis = RedisHelper()
# redis.populate_db()
# players = u.nf_playerlookup()
# players_stats = u.get_feature_scores(players)
# sfp = SimpleFeatureProjector(players_stats)

# for p in players.keys():

# 	print p, sfp.get_projection(p)

from data_collector import NBAStattleShip

ss = NBAStattleShip()
# ss.get_player_stats_data()

rh = RedisHelper()
rh.populate_db()

