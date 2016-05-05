from updater import DailyUpdate
# from projector import SimpleFeatureProjector
from db_helper import RedisHelper

from data_collector import NBAStattleShip


nss = NBAStattleShip()
du = DailyUpdate()


# u = DailyUpdate()
# redis = RedisHelper()
# redis.populate_db()
# players = u.nf_playerlookup()
# players_stats = u.get_feature_scores(players)
# sfp = SimpleFeatureProjector(players_stats)

# for p in players.keys():

# 	print p, sfp.get_projection(p)


rh = RedisHelper()
rh.populate_db()

# nss.get_game_log_data('nba-steven-adams')
# nss.get_game_log_data('nba-jeff-adrien')



