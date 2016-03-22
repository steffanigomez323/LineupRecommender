"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Update Module
"""

from app import redis_db
from models import Player
from app import swish_scraper
from app import nba_scraper
from app import id_manager


class DailyUpdate(object):
    def get_projections(self):
        data = swish_scraper.get_projections()
        projections = swish_scraper.clean_projections(data)
        print "here"
        players = list()

        for projection in projections:
            # rjust to make sure that it is 20 in length
            swish_id = id_manager.get_normalized_swish_id(
                projection['player_id'])
            print "if"
            if redis_db.get(swish_id):
                player_id = redis_db.get(swish_id)
                name = redis_db.hget(player_id, 'name')
                team = redis_db.hget(player_id, 'team')
                position = redis_db.hget(player_id, 'position')
                projected_points = projection['proj_fantasy_pts_fd']
                salary = projection['fd_salary']
                injury_status = projection['injury_status']

                players.append(Player(player_id, name, team, position,
                               projected_points, salary, injury_status))

        print players
        return players


    def get_stats(self):
        data = nba_scraper.get_player_stats()
        player_stats = nba_scraper.clean_player_stats(data)

        print player_stats
