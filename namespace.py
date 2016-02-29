# NAMESPACE #
from app import redis_db
import json
from pprint import pprint

# first player id which gets incremented
FIRST_PLAYER_ID = 123456

# all possible teams
TEAMS = set(['BOS', 'BKN', 'NY', 'PHI',
             'TOR', 'CHI', 'CLE', 'DET',
             'IND', 'MIL', 'ATL', 'CHA',
             'MIA', 'ORL', 'WAS', 'GS',
             'LAC', 'LAL', 'PHO', 'SAC',
             'DAL', 'HOU', 'MEM', 'NO',
             'SA', 'DEN', 'MIN', 'OKC',
             'POR', 'UTA'])

# all possible positions
POSITIONS = set(['PG', 'SG', 'SF', 'PF', 'C'])
