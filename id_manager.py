"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Update Module
"""

from app import redis_db


class IDManager(object):
    # player id which gets incremented
    INITIAL_BASE_PLAYER_ID = '123456'

    def __init__(self):
        pass

    def get_player_id(self, base_id, nba_id, swish_id):
        player_id = base_id.rjust(10, '0') + nba_id.rjust(10, '0') + \
                        swish_id.rjust(10, '0')

        return player_id

    def write_id_mappings(self, nba_id, swish_id, player_id):
        # rjust nba by 10
        nba_rjust = nba_id.rjust(10, '0')
        # rjust swish by 20
        swish_rjust = swish_id.rjust(20, '0')

        redis_db.set(nba_rjust, player_id)
        redis_db.set(swish_rjust, player_id)

    def get_swish_id(self, swish_id):
        return swish_id.rjust(20, '0')

    def get_nba_id(self, nba_id):
        return nba_id.rjust(10, '0')

    def get_player_id_from_swish_id(self, swish_id):
        player_id = redis_db.get(swish_id)
        if not player_id:
            raise Exception("The player does not exist.")

        return player_id

    def get_player_id_from_nba_id(self, nba_id):
        player_id = redis_db.get(nba_id)
        if not player_id:
            raise Exception("The player does not exist.")

        return player_id
