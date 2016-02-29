"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Database
"""

from app import redis_db
from scrapers import SwishScraper
from scrapers import NBAScraper
import namespace as ns


class RedisHelper(object):
    # populate the database with all players using swish
    def populate_db(self):
        # set player_id to 123455
        redis_db.set('player_id', ns.FIRST_PLAYER_ID - 1)

        # add all teams
        for team in ns.TEAMS:
            redis_db.sadd('teams', team)

        # add all positions
        for position in ns.POSITIONS:
            redis_db.sadd('positions', position)

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

    # update each players stats from nba.com
    def populate_stats(self):
        ns = NBAScraper()
        stats = ns.get_player_stats_request()
        player_stats = ns.clean_player_stats_data(stats)

        return player_stats
