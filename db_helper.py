"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Database
"""

from app import redis_db
from app import swish_scraper
from app import nba_scraper
from app import id_manager
import namespace as ns
import re


class RedisHelper(object):
    # populate the database with all players using swish and nba
    def populate_db(self):
        # flush the db
        redis_db.flushall()

        # set base_id to 123455
        redis_db.set('base_id', int(id_manager.INITIAL_BASE_PLAYER_ID) - 1)

        # add all teams
        for team in ns.TEAMS:
            redis_db.sadd('teams', team)

        # add all positions
        for position in ns.POSITIONS:
            redis_db.sadd('positions', position)

        # get all players from nba
        nba_raw = nba_scraper.get_players()
        nba_players = nba_scraper.clean_players(nba_raw)

        # get all players from swish
        swish_raw = swish_scraper.get_players()
        swish_players = swish_scraper.clean_players(swish_raw)

        # get unified player list
        players = self.unify(nba_players, swish_players)

        # write players to redis
        for player, data in players.iteritems():
            team = data[2]
            team_id = data[3]
            position = data[4]

            # increment base_id
            redis_db.incr('base_id')
            base_id = redis_db.get('base_id')

            # get final unique id
            player_id = id_manager.get_player_id(base_id, data[0], data[1])

            # write swish_id to player_id and nba_id to player_id
            # mappings to redis
            id_manager.write_id_maps(data[0], data[1], player_id)

            if not redis_db.sismember('teams', team):
                raise Exception("This player's team does not exist.")

            if not redis_db.sismember('positions', position):
                raise Exception("This player's position is invalid.")

            redis_db.hmset(player_id, {'name': player,
                                       'team': team,
                                       'team_id': team_id,
                                       'position': position})

    def unify(self, nba_players, swish_players):
        unified_dict = {}

        for player_name in swish_players.iterkeys():
            modified_name = player_name
            match = re.search('.\..\.', modified_name)
            if match:
                modified_name = modified_name.replace(".", "")

            if modified_name == "Nene Hilario":
                modified_name = "Nene"
            elif modified_name == "Louis Amundson":
                modified_name = "Lou Amundson"
            elif modified_name == "JJ Barea":
                modified_name = "Jose Juan Barea"
            elif modified_name == "Kelly Oubre Jr.":
                modified_name = "Kelly Oubre"
            elif modified_name == "Glenn Robinson III":
                modified_name = "Glenn Robinson"
            elif modified_name == "Luc Richard Mbah a Moute":
                modified_name = "Luc Mbah a Moute"

            modified_name = modified_name.lower()

            if modified_name in nba_players.iterkeys():
                swish_player = swish_players[player_name]
                nba_player = nba_players[modified_name]
                swish_id = swish_player[0]
                swish_team = swish_player[1]
                if swish_team not in ns.TEAMS:
                    swish_team = ns.SWISH_NBA_TEAM_NAME_MAP[swish_team]
                swish_position = swish_player[2]
                nba_id = nba_player[0]
                nba_team_id = nba_player[1]
                nba_team = nba_player[2]
                nba_name = nba_player[3]

                if nba_team != swish_team:
                    raise Exception("There is a mismatch in the teams.")

                unified_dict[nba_name] = (nba_id, swish_id, nba_team,
                                          nba_team_id, swish_position)

        return unified_dict

    # implement update db
    # def update_db(self):
