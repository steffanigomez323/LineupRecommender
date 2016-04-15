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
from app import fanduel_scorer


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

        # TODO: insert into redis db
        #print fanduel_scorer.score_all_players(player_stats)
        
        return player_stats

    def get_scores(self):
        seasons = ['2015-16', '2014-15', '2013-14', '2012-13']

        raw_scores = {}
        for season in seasons:
            data = nba_scraper.get_player_stats(season)
            player_stats = nba_scraper.clean_player_stats(data)

            season_scores = fanduel_scorer.score_all_players(player_stats)
            for player, info in season_scores.items():
                if player in raw_scores:
                    raw_scores[player]['GAME_SCORES'].extend(info['GAME_SCORES'])
                else:
                    raw_scores[player] = info

        # convert to players ids mapped to a sorted list of scores, by ascending dates
        ordered_scores = {
            info['PLAYER_NAME']:
                sorted(info['GAME_SCORES'], key=lambda g: g['DATE'])
            for k, info in raw_scores.items()}
        player_scores = {
            k:
                [g['SCORE'] for g in games]
            for k, games in ordered_scores.items()}

        return player_scores
