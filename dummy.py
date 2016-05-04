from updater import DailyUpdate
# from projector import SimpleFeatureProjector
from db_helper import RedisHelper

from data_collector import NBAStattleShip


nss = NBAStattleShip()

print nss.prepare_data_for_projections('nba-lebron-james')

