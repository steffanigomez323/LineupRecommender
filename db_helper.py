"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Database
"""

from app import redis_db
from scrapers import SwishScraper


class RedisHelper(object):
    # populate the database with all players
    def populate_db(self):
        # set player_id to 123455
        redis_db.set('player_id', 123455)

        # add all teams
        redis_db.sadd('teams', 'BOS', 'BKN', 'NY', 'PHI',
                      'TOR', 'CHI', 'CLE', 'DET',
                      'IND', 'MIL', 'ATL', 'CHA',
                      'MIA', 'ORL', 'WAS', 'GS',
                      'LAC', 'LAL', 'PHO', 'SAC',
                      'DAL', 'HOU', 'MEM', 'NO',
                      'SA', 'DEN', 'MIN', 'OKC',
                      'POR', 'UTA')

        # add all positions
        redis_db.sadd('positions', 'PG', 'SG', 'SF', 'PF', 'C')

        # add all players
        ss = SwishScraper()
        data = ss.get_players_request()
        players = ss.clean_players_data(data)
        for player in players:
            redis_db.incr('player_id')
            player_id = redis_db.get('player_id')
            swish_id = player['player_id']
            name = player['player_name']
            team = player['team_abbr']
            position = player['primary_pos_abbr']

            if not redis_db.sismember('teams', team):
                raise Exception("This player's team does not exist.")

            if not redis_db.sismember('positions', position):
                raise Exception("This player's position is invalid.")

            redis_db.hmset(player_id, {'swish_id': swish_id,
                                       'name': name,
                                       'team': team,
                                       'position': position})
