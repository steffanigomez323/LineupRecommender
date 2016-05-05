"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Update Module
"""

from app import redis_db
from models import Player
#from app import swish_scraper
#from app import nba_scraper
from app import id_manager
from app import fanduel_scorer
from app import nba_stattleship
from app import nf_scraper
import re
import datetime
import time

class DailyUpdate(object):
    def get_projections(self):
        data = swish_scraper.get_projections()
        projections = swish_scraper.clean_projections(data)
        players = list()

        for projection in projections:
            # rjust to make sure that it is 20 in length
            swish_id = id_manager.get_normalized_swish_id(
                projection['player_id'])

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

    def create_stattleship_games(self, stattleship_id_list):

        games_dict = {}
        count = 1
        for nba_player_id in stattleship_id_list:
            # start_time = time.clock()
            games_data = nba_stattleship.prepare_data_for_projections(nba_player_id)

            if games_data != None:
                list_size = len(games_data['blocks'])

                for i in range(0, list_size):

                    features = {}
                    game_id = re.sub(r'\W', '', games_data['game_time'][i].encode('utf-8')).replace('T', '')
                    features['steals'] = games_data['steals'][i]
                    features['assists'] = games_data['assists'][i]
                    features['rebounds_total'] = games_data['rebounds_total'][i]
                    features['points'] = games_data['points'][i]
                    features['turnovers'] = games_data['turnovers'][i]
                    features['blocks'] = games_data['blocks'][i]
                    features['min_PG'] = games_data['time_played_total'][i] / 60
                    features['plus_minus_PG'] = games_data['plus_minus'][i]
                    features['hva'] = 'home' if games_data['played_at_home'][i] == 'True' else 'away'
                    features['opponent'] = games_data['played_against'][i].encode('utf-8')
                    games_dict[game_id] = features

                # end_time = time.clock()
                print nba_player_id, count
            count += 1

        return games_dict

    def store_stattleship_gamelogs(self, stattleship_gamelogs):
        TIME_ID_LEN = 19 # length of time component of id, ex: -201602011900000500
        
        player_games = {}
        for player_game_id, player_gamelogs in stattleship_gamelogs.items():
            '''
            player_gamelogs['steals_pg']
            player_gamelogs['rebounds_pg']
            player_gamelogs['points_pg']
            player_gamelogs['turnovers_pg']
            player_gamelogs['blocks_pg']
            player_gamelogs['minutes_pg']
            player_gamelogs['plus_minus_pg']
            player_gamelogs['hva']
            player_gamelogs['opponent']
            player_gamelogs['time_stamp']
            '''
            redis_db.hmset(player_game_id, player_gamelogs)

            # generate player_id to games_id mapping
            player_id = player_game_id[:-TIME_ID_LEN]
            games_list = player_games.get(player_id, default=[])
            games_list.append(player_game_id)
            player_games[player_id] = games_list

        for player_id, games_list in player_games.items():
            redis_db.lpush(player_id, *games_list) #pass in list as arguments using *args syntax

    def nf_playerlookup(self):
        player_data = nf_scraper.get_todays_player_data()
        players = {}
        for p in player_data:
            data = redis_db.hgetall("nba-" + p[0])
            if (len(data) == 0):
                data.update(redis_db.hgetall("nba-" + redis_db.get(p[0])))
                players["nba-" + redis_db.get(p[0])] = data
            else:
                players["nba-" + p[0]] = data
        return players

    def get_feature_scores(self, players):
        players = players.keys()
        player_stats = {}
        for player in players:

            data = nba_stattleship.prepare_data_for_projections(player)

            points_tup = zip(data["game_time"], data["points"])
            rebounds_tup = zip(data["game_time"], data["rebounds_total"])
            steals_tup = zip(data["game_time"], data["steals"])
            assists_tup = zip(data["game_time"], data["assists"])
            turnovers_tup = zip(data["game_time"], data["turnovers"])
            blocks_tup = zip(data["game_time"], data["blocks"])

            points_tup_sort = []
            rebounds_tup_sort = []
            steals_tup_sort = []
            assists_tup_sort = []
            turnovers_tup_sort = []
            blocks_tup_sort = []
            for i in range(0, len(points_tup)):
                time = points_tup[i][0][0:10].split("-")
                day = datetime.date(int(time[0]), int(time[1]), int(time[2]))
                points_tup_sort.append((day, points_tup[i][1]))
                rebounds_tup_sort.append((day, rebounds_tup[i][1]))
                steals_tup_sort.append((day, steals_tup[i][1]))
                assists_tup_sort.append((day, assists_tup[i][1]))
                turnovers_tup_sort.append((day, turnovers_tup[i][1]))
                blocks_tup_sort.append((day, blocks_tup[i][1]))

            points_tup_sort.sort(key=lambda tup: tup[0])
            rebounds_tup_sort.sort(key=lambda tup: tup[0])
            steals_tup_sort.sort(key=lambda tup: tup[0])
            assists_tup_sort.sort(key=lambda tup: tup[0])
            turnovers_tup_sort.sort(key=lambda tup: tup[0])
            blocks_tup_sort.sort(key=lambda tup: tup[0])


            if len(points_tup_sort) == 0:
                continue

            d, points = zip(*points_tup_sort)
            d, rebounds = zip(*rebounds_tup_sort)
            d, steals = zip(*steals_tup_sort)
            d, assists = zip(*assists_tup_sort)
            d, turnovers = zip(*turnovers_tup_sort)
            d, blocks = zip(*blocks_tup_sort)


            player_stats[player] = {
            "points": list(points),
            "rebounds": list(rebounds),
            "steals": list(steals),
            "assists": list(assists),
            "turnovers": list(turnovers),
            "blocks": list(blocks),
            "dates": list(d)}
        return player_stats
