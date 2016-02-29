# NAMESPACE #
from app import redis_db

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

# dictionary from name to player_id
NAME_TO_PLAYER_ID = {}

# dictionary from nba_id to player_id
NBA_ID_TO_PLAYER_ID = {}


def gen_nba_relation_dict():
    last_player_id = redis_db.get('player_id')
    for player_id in range(FIRST_PLAYER_ID, last_player_id + 1):
        name = redis_db.hmget(player_id, 'name')
        NAME_TO_PLAYER_ID[name] = player_id

        # go over the json
        # check if name exists in NAME_TO_PLAYER_ID
        # print it if it does not exist
        # if it does exist, set NBA_ID_TO_PLAYER_ID[nba_id] to
        # player_id which you can get from NAME_TO_PLAYER_ID


if __name__ == '__main__':
    gen_nba_relation_dict()
