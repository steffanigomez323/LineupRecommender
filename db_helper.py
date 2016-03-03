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
import namespace
import json
import re


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
        # dictionary from name to player_id
        NAME_TO_PLAYER_ID = {}

        # dictionary from nba_id to player_id
        NBA_ID_TO_PLAYER_ID = {}

        ns = NBAScraper()
        stats = ns.get_player_stats_request()
        player_stats = ns.clean_player_stats_data(stats)

        # player_json = open('players.json', 'r')
        # player_stats = json.load(player_json)

        last_player_id = int(redis_db.get('player_id'))

        for player_id in range(namespace.FIRST_PLAYER_ID, last_player_id + 1):
            name = redis_db.hmget(player_id, 'name')

            player_name = name[0]
            match = re.search('.\..\.', player_name)
            if match:
                player_name = player_name.replace(".", "")

            if player_name == "Nene Hilario":
                player_name = "Nene"
            elif player_name == "Louis Amundson":
                player_name = "Lou Amundson"
            elif player_name == "JJ Barea":
                player_name = "Jose Juan Barea"
            elif player_name == "Kelly Oubre Jr.":
                player_name = "Kelly Oubre"
            elif player_name == "Glenn Robinson III":
                player_name = "Glenn Robinson"
            elif player_name == "Luc Richard Mbah a Moute":
                player_name = "Luc Mbah a Moute"

            player_name = player_name.lower()

            NAME_TO_PLAYER_ID[player_name] = player_id

        # check if name exists in NAME_TO_PLAYER_ID
        for nba_id in player_stats:
            # player_stats[nba_id] returns dictionaries of games
            nba_name = player_stats[nba_id]['PLAYER_NAME']
            match = re.search('.\..\.', nba_name)
            if match:
                nba_name = nba_name.replace(".", "")

            nba_name = nba_name.lower()

            if nba_name in NAME_TO_PLAYER_ID.iterkeys():
                NBA_ID_TO_PLAYER_ID[nba_id] = NAME_TO_PLAYER_ID[nba_name]
                # print "MATCHED: ", nba_name

        # print it if it does not exist
            else:
                print "NOT MATCHED: ", nba_name

