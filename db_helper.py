"""
CS1951A Final Project
Brown University
Spring 2015

Vann, Steffani, JJ, Chaitu

Database
"""

from app import app
from scrapers import SwishScraper


class RedisHelper(object):
    # populate the database with all players
    def populate_db(self):
        # add all teams
        app.database.sadd('teams', 'BOS', 'BKN', 'NY', 'PHI',
                          'TOR', 'CHI', 'CLE', 'DET',
                          'IND', 'MIL', 'ATL', 'CHA',
                          'MIA', 'ORL', 'WAS', 'GS',
                          'LAC', 'LAL', 'PHO', 'SAC',
                          'DAL', 'HOU', 'MEM', 'NO',
                          'SA', 'DEN', 'MIN', 'OKC',
                          'POR', 'UTA')

        # add all positions
        app.database.sadd('positions', 'PG', 'SG', 'SF', 'PF', 'C')

        # add all players
        ss = SwishScraper()
        data = ss.get_players_request()
        players = ss.clean_players_data(data)
        for player in players:
            player_id = player['player_id']
            name = player['player_name']
            team = player['team_abbr']
            position = player['primary_pos_abbr']

            if not app.database.sismember('teams', team):
                raise Exception("This player's team does not exist.")

            if not app.database.sismember('positions', position):
                raise Exception("This player's position is invalid.")

            app.database.hmset(player_id, {'name': name,
                                           'team': team,
                                           'position': position})
