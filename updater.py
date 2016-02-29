"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Update Module
"""

from app import redis_db
from models import Player
from scrapers import SwishScraper
from scrapers import NBAScraper


class DailyUpdate(object):
    def get_update(self):
        ss = SwishScraper()
        data = ss.get_projections_request()
        projections = ss.clean_projections_data(data)
        players = list()

        for projection in projections:
            player_id = projection['player_id']
            name = projection['player_name']
            stored_name = redis_db.hget(player_id, 'name')
            if stored_name != name:
                redis_db.hset(player_id, 'name', name)
            team = projection['team_abr']
            stored_team = redis_db.hget(player_id, 'team')
            if stored_team != team:
                redis_db.hset(player_id, 'team', team)
            position = projection['fd_pos']
            stored_position = redis_db.hget(player_id, 'position')
            if stored_position != position:
                redis_db.hset(player_id, 'position', position)
            projected_points = projection['proj_fantasy_pts_fd']
            salary = projection['fd_salary']
            injury_status = projection['injury_status']

            players.append(Player(player_id, name, team, position,
                           projected_points, salary, injury_status))

        return players
