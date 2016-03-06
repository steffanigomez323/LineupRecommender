"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

ID Manager
"""


class IDManager(object):
    # player id which gets incremented
    INITIAL_BASE_PLAYER_ID = '123456'

    def get_player_id(self, base_id, nba_id, swish_id):
        player_id = base_id.rjust(10, '0') + nba_id.rjust(10, '0') + \
                        swish_id.rjust(10, '0')

        return player_id

    def get_normalized_swish_id(self, swish_id):
        return swish_id.rjust(20, '0')

    def get_normalized_nba_id(self, nba_id):
        return nba_id.rjust(10, '0')
