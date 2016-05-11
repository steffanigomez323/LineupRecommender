"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Player Performance Projector
"""

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
import operator
from collections import Counter
from scorer import FanDuelScorer
import numpy as np
from copy import deepcopy
from app import nf_scraper
from db_helper import CSVHelper
from namespace import Namespace

'''
class SimpleProjector(object):

    def __init__(self, players):
        self.players = players
        self.avg = lambda x: sum(x) / float(len(x))

    def print_all_players(self):
        for player in self.players:
            print player

    def get_models(self, num_games):
        last_n_dict = {}
        for player in self.players.iterkeys():
            last_n_dict[player] = {}
            for i in range(1, num_games):
                last_n_dict[player][i] = [[], []]
                scores = self.players[player]
                for j in range(i, len(scores)):
                    last_n_dict[player][i][0].append(scores[j])
                    last_n_dict[player][i][1].append(self.avg(scores[j - i:j]))
        return last_n_dict

    def get_best_last_n(self, last_n_dict, num_games):
        r2_dict = {}
        for player in last_n_dict.iterkeys():
            r2_dict[player] = {}
            for last_n in last_n_dict[player].iterkeys():
                if len(last_n_dict[player][last_n][0]) > 0:
                    assert len(last_n_dict[player][last_n][0]) == len(
                        last_n_dict[player][last_n][1])
                    r2_dict[player][last_n] = r2_score(
                        last_n_dict[player][last_n][0], last_n_dict[player][last_n][1])

        count_14s = 0
        last_ns = []
        for player, last_n in r2_dict.iteritems():
            if len(last_n) == num_games - 1:
                count_14s += 1
                last_ns.append(
                    max(last_n.iteritems(), key=operator.itemgetter(1))[0])

        data = Counter(last_ns)
        return data.most_common(1)[0][0]

    def get_projection(self, scores, averages, last_n):
        classifier = LogisticRegression()
        # print "#### SCORES"
        # print scores
        # print "#### AVERAGES"
        # print averages
        classifier.fit(numpy.array([numpy.array([average]) for average in averages]), numpy.array(
            [int(score) for score in scores]))
        return classifier.predict(self.avg(scores[::-last_n]))


class SimpleFeatureProjector(object):
    BEST_N_MAX = 14

    POINT_ID = 'points'
    STEAL_ID = 'steals'
    ASSIST_ID = 'assists'
    REBOUND_ID = 'rebounds'
    TURNOVER_ID = 'turnovers'
    BLOCK_ID = 'blocks'

    def __init__(self, players):
        self.players = players

    def get_projection(self, player_id):
        print "Getting projection for " + player_id

        pts = self.project_points(player_id)
        stl = self.project_steals(player_id)
        ast = self.project_assists(player_id)
        reb = self.project_rebounds(player_id)
        tov = self.project_turnovers(player_id)
        blk = self.project_blocks(player_id)

        game = dict()
        game['3PT_FG'] = 0
        game['2PT_FG'] = 0
        game['FT'] = 0
        game['REB'] = reb
        game['AST'] = ast
        game['BLK'] = blk
        game['STL'] = stl
        game['TOV'] = tov

        total_score = FanDuelScorer.find_fanduel_score(game)
        total_score += pts

        return {'points': pts,
                'steals': stl,
                'assists': ast,
                'rebounds': reb,
                'turnovers': tov,
                'blocks': blk,
                'score': total_score}

    def project_feature(self, feature_id, player_id):
        player_features = {k: v[feature_id] for k, v in self.players.items()}

        sp = SimpleProjector(player_features)
        player_models = sp.get_models(self.BEST_N_MAX)
        best_last_n = sp.get_best_last_n(player_models, self.BEST_N_MAX)

        scores = player_models[player_id][best_last_n][0]
        averages = player_models[player_id][best_last_n][1]

        print "Best N value for " + feature_id + ": ", best_last_n

        return sp.get_projection(scores, averages, best_last_n)[0]

    def project_points(self, player_id):
        return self.project_feature(self.POINT_ID, player_id)

    def project_steals(self, player_id):
        return self.project_feature(self.STEAL_ID, player_id)

    def project_assists(self, player_id):
        return self.project_feature(self.ASSIST_ID, player_id)

    def project_rebounds(self, player_id):
        return self.project_feature(self.REBOUND_ID, player_id)

    def project_turnovers(self, player_id):
        return self.project_feature(self.TURNOVER_ID, player_id)

    def project_blocks(self, player_id):
        return self.project_feature(self.BLOCK_ID, player_id)
'''

class FeatureCreator(object):
    POINTS_IDX = 10
    REBOUNDS_IDX = 5
    ASSISTS_IDX = 6
    STEALS_IDX = 7
    BLOCKS_IDX = 8
    TURNOVERS_IDX = 9
    TIME_IDX = 4
    OPPONENT_IDX = 1
    HVA_IDX = 2
    PLUS_MINUS_IDX = 3

    OPPONENT_LIST = [x for x in Namespace.TEAM_MAP_NF_NBA.itervalues()]
    OPPONENT_LIST.pop()
    POSITION_LIST = [x for x in Namespace.POSITIONS]
    #POSITION_LIST.pop()

    TRUE_NUM = 1
    FALSE_NUM = 0

    SCORER = lambda self, x: x['points'] + x['rebounds']*1.2 + x['assists']*1.5 + \
        x['blocks']*2 + x['steals']*2 - x['turnovers']

    # take in pos, height, gamelogs
    # {id: {position: ssfd, height:fasdf}}
    def __init__(self, players_gamelogs, upcoming_games):
        self.avg = lambda x: sum(x) / float(len(x))

        self.players_gamelogs = players_gamelogs
        self.upcoming_games = upcoming_games

        self.all_training_features = None
        self.all_training_fanduel = None
        self.all_average_fanduel = None

    def __append_features(self, target, append_array):
        if len(append_array) == 0:
            return target
        elif target is None:
            return append_array
        else:
            return np.vstack((target, append_array))

    def calc_all_training_features(self):
        all_features = {"assists": None,
                        "points": None,
                        "blocks": None,
                        "rebounds": None,
                        "turnovers": None,
                        "steals": None}

        for pid in self.players_gamelogs.iterkeys():
            if len(self.players_gamelogs[pid]['gamelogs']) == 0:
                continue

            features = self.get_player_training_features(pid)

            for k, v in features.iteritems():
                all_features[k] = self.__append_features(all_features[k], v)

        return all_features

    def calc_all_training_fanduel(self):
        all_features = {"fanduel": None}

        for pid in self.players_gamelogs.iterkeys():
            if len(self.players_gamelogs[pid]['gamelogs']) == 0:
                continue

            features = self.get_player_training_fanduel(pid)

            for k, v in features.iteritems():
                all_features[k] = self.__append_features(all_features[k], v)

        return all_features

    def calc_some_training_features(self, player_ids):
        all_features = {"assists": None,
                        "points": None,
                        "blocks": None,
                        "rebounds": None,
                        "turnovers": None,
                        "steals": None}

        for pid in player_ids:
            if len(self.players_gamelogs[pid]['gamelogs']) == 0:
                continue

            features = self.get_player_training_features(pid)

            for k, v in features.iteritems():
                all_features[k] = self.__append_features(all_features[k], v)

        return all_features

    def calc_some_training_fanduel(self, player_ids):
        all_features = {"fanduel": None}

        for pid in player_ids:
            if len(self.players_gamelogs[pid]['gamelogs']) == 0:
                continue

            features = self.get_player_training_fanduel(pid)

            for k, v in features.iteritems():
                all_features[k] = self.__append_features(all_features[k], v)

        return all_features

    def calc_player_training_features(self, player_id):
        position = self.players_gamelogs[player_id]['position']
        height = float(self.players_gamelogs[player_id]['height'])

        gamelog = self.players_gamelogs[player_id]['gamelogs']
        gamelog = np.array(gamelog)

        points = gamelog[:, self.POINTS_IDX].astype(np.float)
        rebounds = gamelog[:, self.REBOUNDS_IDX].astype(np.float)
        assists = gamelog[:, self.ASSISTS_IDX].astype(np.float)
        steals = gamelog[:, self.STEALS_IDX].astype(np.float)
        blocks = gamelog[:, self.BLOCKS_IDX].astype(np.float)
        turnovers = gamelog[:, self.TURNOVERS_IDX].astype(np.float)
        time = gamelog[:, self.TIME_IDX].astype(np.float)
        plus_minus = gamelog[:, self.PLUS_MINUS_IDX].astype(np.float)
        opponent = gamelog[:, self.OPPONENT_IDX]
        hva = gamelog[:, self.HVA_IDX]

        num_logs = len(points)

        # points
        points_train = []
        for i in range(7, num_logs):
            row = [points[i],  # label
                   self.avg(points[i - 1:i]),  # last 1
                   self.avg(points[i - 3:i]),  # last 3
                   self.avg(points[i - 5:i]),  # last 5
                   self.avg(points[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i])]  # time avg

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            points_train.append(row)

        # assists
        assists_train = []
        for i in range(7, num_logs):
            row = [assists[i],  # label
                   self.avg(assists[i - 1:i]),  # last 1
                   self.avg(assists[i - 3:i]),  # last 3
                   self.avg(assists[i - 5:i]),  # last 5
                   self.avg(assists[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i])]  # time avg

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            assists_train.append(row)

        # steals
        steals_train = []
        for i in range(7, num_logs):
            row = [steals[i],  # label
                   self.avg(steals[i - 1:i]),  # last 1
                   self.avg(steals[i - 3:i]),  # last 3
                   self.avg(steals[i - 5:i]),  # last 5
                   self.avg(steals[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i])]  # time avg

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            steals_train.append(row)

        # turnovers
        turnovers_train = []
        for i in range(7, num_logs):
            row = [turnovers[i],  # labels
                   self.avg(turnovers[i - 1:i]),  # last 1
                   self.avg(turnovers[i - 3:i]),  # last 3
                   self.avg(turnovers[i - 5:i]),  # last 5
                   self.avg(turnovers[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i])]  # time avg

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            turnovers_train.append(row)

        # rebounds
        rebounds_train = []
        for i in range(7, num_logs):
            row = [rebounds[i],  # label
                   self.avg(rebounds[i - 1:i]),  # last 1
                   self.avg(rebounds[i - 3:i]),  # last 3
                   self.avg(rebounds[i - 5:i]),  # last 5
                   self.avg(rebounds[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i]),  # time avg
                   height]  # height

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            rebounds_train.append(row)

        # blocks
        blocks_train = []
        for i in range(7, num_logs):
            row = [blocks[i],  # label
                   self.avg(blocks[i - 1:i]),  # last 1
                   self.avg(blocks[i - 3:i]),  # last 3
                   self.avg(blocks[i - 5:i]),  # last 5
                   self.avg(blocks[i - 7:i]),  # last 7
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i]),  # time avg
                   height]  # height

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            blocks_train.append(row)

        return {"assists": np.array(assists_train),
                "points": np.array(points_train),
                "blocks": np.array(blocks_train),
                "rebounds": np.array(rebounds_train),
                "turnovers": np.array(turnovers_train),
                "steals": np.array(steals_train)}

    def calc_player_projection_features(self, player_id):
        position = self.players_gamelogs[player_id]['position']
        height = float(self.players_gamelogs[player_id]['height'])

        gamelog = self.players_gamelogs[player_id]['gamelogs']
        gamelog = np.array(gamelog)

        opponent = self.upcoming_games[player_id]['playing_against']
        hva = self.upcoming_games[player_id]['playing_at_home']

        points = gamelog[:, self.POINTS_IDX].astype(np.float)
        rebounds = gamelog[:, self.REBOUNDS_IDX].astype(np.float)
        assists = gamelog[:, self.ASSISTS_IDX].astype(np.float)
        steals = gamelog[:, self.STEALS_IDX].astype(np.float)
        blocks = gamelog[:, self.BLOCKS_IDX].astype(np.float)
        turnovers = gamelog[:, self.TURNOVERS_IDX].astype(np.float)
        time = gamelog[:, self.TIME_IDX].astype(np.float)
        plus_minus = gamelog[:, self.PLUS_MINUS_IDX].astype(np.float)

        # transform the categorical data
        hva_num = (self.TRUE_NUM if hva == "True" else self.FALSE_NUM)
        opponent_nums = [self.TRUE_NUM if x == opponent else self.FALSE_NUM
                         for x in self.OPPONENT_LIST]
        position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                         for x in self.POSITION_LIST]

        i = len(points)

        # points
        points_proj = [self.avg(points[i - 1:i]),  # last 1
                       self.avg(points[i - 3:i]),  # last 3
                       self.avg(points[i - 5:i]),  # last 5
                       self.avg(points[i - 7:i]),  # last 7
                       self.avg(plus_minus[0:i]),  # plus minus avg
                       self.avg(time[0:i])]  # time avg
        points_proj.append(hva_num)
        points_proj.extend(opponent_nums)
        points_proj.extend(position_nums)

        # assists
        assists_proj = [self.avg(assists[i - 1:i]),  # last 1
                        self.avg(assists[i - 3:i]),  # last 3
                        self.avg(assists[i - 5:i]),  # last 5
                        self.avg(assists[i - 7:i]),  # last 7
                        self.avg(plus_minus[0:i]),  # plus minus avg
                        self.avg(time[0:i])]  # time avg
        assists_proj.append(hva_num)
        assists_proj.extend(opponent_nums)
        assists_proj.extend(position_nums)

        # steals
        steals_proj = [self.avg(steals[i - 1:i]),  # last 1
                       self.avg(steals[i - 3:i]),  # last 3
                       self.avg(steals[i - 5:i]),  # last 5
                       self.avg(steals[i - 7:i]),  # last 7
                       self.avg(plus_minus[0:i]),  # plus minus avg
                       self.avg(time[0:i])]  # time avg
        steals_proj.append(hva_num)
        steals_proj.extend(opponent_nums)
        steals_proj.extend(position_nums)

        # turnovers
        turnovers_proj = [self.avg(turnovers[i - 1:i]),  # last 1
                          self.avg(turnovers[i - 3:i]),  # last 3
                          self.avg(turnovers[i - 5:i]),  # last 5
                          self.avg(turnovers[i - 7:i]),  # last 7
                          self.avg(plus_minus[0:i]),  # plus minus avg
                          self.avg(time[0:i])]  # time avg
        turnovers_proj.append(hva_num)
        turnovers_proj.extend(opponent_nums)
        turnovers_proj.extend(position_nums)

        # rebounds
        rebounds_proj = [self.avg(rebounds[i - 1:i]),  # last 1
                         self.avg(rebounds[i - 3:i]),  # last 3
                         self.avg(rebounds[i - 5:i]),  # last 5
                         self.avg(rebounds[i - 7:i]),  # last 7
                         self.avg(plus_minus[0:i]),  # plus minus avg
                         self.avg(time[0:i]),  # time avg
                         height]  # height
        rebounds_proj.append(hva_num)
        rebounds_proj.extend(opponent_nums)
        rebounds_proj.extend(position_nums)

        # blocks
        blocks_proj = [self.avg(blocks[i - 1:i]),  # last 1
                       self.avg(blocks[i - 3:i]),  # last 3
                       self.avg(blocks[i - 5:i]),  # last 5
                       self.avg(blocks[i - 7:i]),  # last 7
                       self.avg(plus_minus[0:i]),  # plus minus avg
                       self.avg(time[0:i]),  # time avg
                       height]  # height
        blocks_proj.append(hva_num)
        blocks_proj.extend(opponent_nums)
        blocks_proj.extend(position_nums)

        return {"assists": np.array(assists_proj).reshape(1, -1),
                "points": np.array(points_proj).reshape(1, -1),
                "blocks": np.array(blocks_proj).reshape(1, -1),
                "rebounds": np.array(rebounds_proj).reshape(1, -1),
                "turnovers": np.array(turnovers_proj).reshape(1, -1),
                "steals": np.array(steals_proj).reshape(1, -1)}

    def calc_player_training_fanduel(self, player_id):
        position = self.players_gamelogs[player_id]['position']
        height = float(self.players_gamelogs[player_id]['height'])

        gamelog = self.players_gamelogs[player_id]['gamelogs']
        gamelog = np.array(gamelog)

        points = gamelog[:, self.POINTS_IDX].astype(np.float)
        rebounds = gamelog[:, self.REBOUNDS_IDX].astype(np.float)
        assists = gamelog[:, self.ASSISTS_IDX].astype(np.float)
        steals = gamelog[:, self.STEALS_IDX].astype(np.float)
        blocks = gamelog[:, self.BLOCKS_IDX].astype(np.float)
        turnovers = gamelog[:, self.TURNOVERS_IDX].astype(np.float)
        time = gamelog[:, self.TIME_IDX].astype(np.float)
        plus_minus = gamelog[:, self.PLUS_MINUS_IDX].astype(np.float)
        opponent = gamelog[:, self.OPPONENT_IDX]
        hva = gamelog[:, self.HVA_IDX]

        num_logs = len(points)

        # aggregate fanduel scores
        fanduel = []
        for i in range(0, num_logs):
            curr_game  = {'assists': assists[i],
                          'rebounds': rebounds[i],
                          'steals': steals[i],
                          'blocks': blocks[i],
                          'turnovers': turnovers[i],
                          'points': points[i]}
            fanduel.append(self.SCORER(curr_game))

        # fanduel training
        fanduel_train = []
        for i in range(10, num_logs):
            row = [fanduel[i],  # label
                   self.avg(fanduel[i - 1:i]),  # last 1
                   self.avg(fanduel[i - 3:i]),  # last 3
                   self.avg(fanduel[i - 5:i]),  # last 5
                   self.avg(fanduel[i - 10:i]),  # last 10
                   self.avg(plus_minus[0:i]),  # plus minus avg
                   self.avg(time[0:i]),  # time avg
                   self.avg(turnovers[0:i])] # TO avg

            hva_num = (self.TRUE_NUM if hva[i] == "True" else self.FALSE_NUM)
            opponent_nums = [self.TRUE_NUM if x == opponent[i] else self.FALSE_NUM
                             for x in self.OPPONENT_LIST]
            position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                             for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            row.extend(position_nums) # position

            fanduel_train.append(row)

        return {"fanduel": np.array(fanduel_train)}

    def calc_player_projection_fanduel(self, player_id):
        position = self.players_gamelogs[player_id]['position']
        height = float(self.players_gamelogs[player_id]['height'])

        gamelog = self.players_gamelogs[player_id]['gamelogs']
        gamelog = np.array(gamelog)

        opponent = self.upcoming_games[player_id]['playing_against']
        hva = self.upcoming_games[player_id]['playing_at_home']

        points = gamelog[:, self.POINTS_IDX].astype(np.float)
        rebounds = gamelog[:, self.REBOUNDS_IDX].astype(np.float)
        assists = gamelog[:, self.ASSISTS_IDX].astype(np.float)
        steals = gamelog[:, self.STEALS_IDX].astype(np.float)
        blocks = gamelog[:, self.BLOCKS_IDX].astype(np.float)
        turnovers = gamelog[:, self.TURNOVERS_IDX].astype(np.float)
        time = gamelog[:, self.TIME_IDX].astype(np.float)
        plus_minus = gamelog[:, self.PLUS_MINUS_IDX].astype(np.float)

        # transform the categorical data
        hva_num = (self.TRUE_NUM if hva == "True" else self.FALSE_NUM)
        opponent_nums = [self.TRUE_NUM if x == opponent else self.FALSE_NUM
                         for x in self.OPPONENT_LIST]
        position_nums = [self.TRUE_NUM if x in position else self.FALSE_NUM
                         for x in self.POSITION_LIST]

        i = len(points)

        # aggregate fanduel scores
        fanduel = []
        for j in range(0, i):
            curr_game  = {'assists': assists[j],
                          'rebounds': rebounds[j],
                          'steals': steals[j],
                          'blocks': blocks[j],
                          'turnovers': turnovers[j],
                          'points': points[j]}
            fanduel.append(self.SCORER(curr_game))

        # fanduel
        fanduel_proj = [self.avg(fanduel[i - 1:i]),  # last 1
                        self.avg(fanduel[i - 3:i]),  # last 3
                        self.avg(fanduel[i - 5:i]),  # last 5
                        self.avg(fanduel[i - 10:i]),  # last 10
                        self.avg(plus_minus[0:i]),  # plus minus avg
                        self.avg(time[0:i]),  # time avg
                        self.avg(turnovers[0:i])] # TO avg
        fanduel_proj.append(hva_num)
        fanduel_proj.extend(opponent_nums)
        fanduel_proj.extend(position_nums)

        return {"fanduel": np.array(fanduel_proj).reshape(1, -1)}

    def calc_player_average_fanduel(self, player_id):
        gamelog = self.players_gamelogs[player_id]['gamelogs']
        gamelog = np.array(gamelog)

        points = gamelog[:, self.POINTS_IDX].astype(np.float)
        rebounds = gamelog[:, self.REBOUNDS_IDX].astype(np.float)
        assists = gamelog[:, self.ASSISTS_IDX].astype(np.float)
        steals = gamelog[:, self.STEALS_IDX].astype(np.float)
        blocks = gamelog[:, self.BLOCKS_IDX].astype(np.float)
        turnovers = gamelog[:, self.TURNOVERS_IDX].astype(np.float)

        num_logs = len(points)

        # aggregate fanduel scores
        fanduel = 0
        for i in range(0, num_logs):
            curr_game  = {'assists': assists[i],
                          'rebounds': rebounds[i],
                          'steals': steals[i],
                          'blocks': blocks[i],
                          'turnovers': turnovers[i],
                          'points': points[i]}
            fanduel += self.SCORER(curr_game)

        return (fanduel / float(num_logs))

    def calc_all_average_fanduel(self):
        all_pid = []
        all_averages = []

        for pid in self.players_gamelogs.iterkeys():
            if len(self.players_gamelogs[pid]['gamelogs']) == 0:
                continue

            average = self.get_player_average_fanduel(pid)

            all_pid.append(pid)
            all_averages.append(average)

        return {'fanduel': zip(all_averages, all_pid)}

    def get_all_training_features(self):
        if self.all_training_features is None:
            self.all_training_features = \
                self.calc_all_training_features()

        return self.all_training_features

    def get_all_training_fanduel(self):
        if self.all_training_fanduel is None:
            self.all_training_fanduel = \
                self.calc_all_training_fanduel()

        return self.all_training_fanduel

    def get_all_average_fanduel(self):
        if self.all_average_fanduel is None:
            self.all_average_fanduel = \
                self.calc_all_average_fanduel()

        return self.all_average_fanduel

    def get_some_training_features(self, player_ids):
        return self.calc_some_training_features(player_ids)

    def get_some_training_fanduel(self, player_ids):
        return self.calc_some_training_fanduel(player_ids)

    def get_player_training_features(self, player_id):
        return self.calc_player_training_features(player_id)

    def get_player_projection_features(self, player_id):
        return self.calc_player_projection_features(player_id)

    def get_player_training_fanduel(self, player_id):
        return self.calc_player_training_fanduel(player_id)

    def get_player_projection_fanduel(self, player_id):
        return self.calc_player_projection_fanduel(player_id)

    def get_player_average_fanduel(self, player_id):
        return self.calc_player_average_fanduel(player_id)

class FeatureProjector(object):
    STAT_FEATURES = ['points', 'assists', 'rebounds', 'blocks', 'steals', 'turnovers']
    FD_FEATURES = ['fanduel']

    SCORER = lambda self, x: x['points'] + x['rebounds']*1.2 + x['assists']*1.5 + \
        x['blocks']*2 + x['steals']*2 - x['turnovers']

    # take in pos, height, gamelogs
    # {id: {position: ssfd, height:fasdf}}
    def __init__(self, feature_creator, regression_maker):
        self.regression_maker = regression_maker

        self.feature_creator = feature_creator

        self.feature_scalers = {}
        self.feature_regressors = {}

    def __split_train_xy(self, training_feature):
        y, X = np.hsplit(  # split off first column (labels)
            training_feature,
            [1])

        return X, np.ravel(y)

    def __split_train_test(self, X, y, test_percent):
        return train_test_split(
            X, y,
            test_size=test_percent, random_state=42)

    def fit_all(self):
        fc = self.feature_creator

        r2_score = {}

        sf = fc.get_all_training_features()
        for fid in self.STAT_FEATURES:
            r2_score[fid] = self.fit_feature(fid, sf)

        ff = fc.get_all_training_fanduel()
        for fid in self.FD_FEATURES:
            r2_score[fid] = self.fit_feature(fid, ff)

        return r2_score

    def fit_player(self, player_id):
        fc = self.feature_creator

        r2_score = {}

        sf = fc.get_player_training_features(player_id)
        for fid in self.STAT_FEATURES:
            r2_score[fid] = self.fit_feature(fid, sf)

        ff = fc.get_player_training_fanduel(player_id)
        for fid in self.FD_FEATURES:
            r2_score[fid] = self.fit_feature(fid, ff)

        return r2_score

    def fit_feature(self, feature_id, features):
        X, y = self.__split_train_xy(features[feature_id])

        self.feature_scalers[feature_id] = StandardScaler()
        scaler = self.feature_scalers[feature_id].fit(X)
        X = scaler.transform(X)

        x_train, x_test, y_train, y_test = \
            self.__split_train_test(X, y, 0.25)

        self.feature_regressors[feature_id] = \
            self.regression_maker()
        regr = self.feature_regressors[feature_id].fit(x_train, y_train)

        score = regr.score(x_test, y_test)
        return score

    def project_feature(self, feature_id, projections):
        x_proj = projections[feature_id]

        scaler = self.feature_scalers[feature_id]
        x_proj = scaler.transform(x_proj)

        regr = self.feature_regressors[feature_id]

        proj = regr.predict(x_proj)
        return proj[0]

    def get_fanduel_score(self, stats_projections):
        projected_scores = {k: v for k,v in stats_projections.iteritems()}
        return self.SCORER(projected_scores)

    def get_stat_projection(self, player_id):
        fc = self.feature_creator

        projections = fc.get_player_projection_features(player_id)

        ast_proj = self.project_feature('assists', projections)

        blk_proj = self.project_feature('blocks', projections)

        stl_proj = self.project_feature('steals', projections)

        pts_proj = self.project_feature('points', projections)

        reb_proj = self.project_feature('rebounds', projections)

        tov_proj = self.project_feature('turnovers', projections)

        return {"assists": ast_proj,
                "points": pts_proj,
                "blocks": blk_proj,
                "rebounds": reb_proj,
                "turnovers": tov_proj,
                "steals": stl_proj}

    def get_fanduel_projection(self, player_id):
        fc = self.feature_creator

        projections = fc.get_player_projection_fanduel(player_id)

        proj = self.project_feature('fanduel', projections)

        return {"fanduel": proj}

class ClusteringFeatureProjector(FeatureProjector):
    def __init__(self, feature_creator, regression_maker, n_clusters=3):
        super(ClusteringFeatureProjector, self).__init__(
            feature_creator,
            regression_maker)

        self.clusterer = KMeans(n_clusters=n_clusters)
        self.feature_regressors_clustered = {}

    def fit_all_clusters(self):
        fc = self.feature_creator

        fd_avg = fc.get_all_average_fanduel()
        X, pids = zip(*fd_avg['fanduel'])
        X = np.array([X]).T # turn into numpy 1-row matrix, and transpose

        cluster_labels = self.clusterer.fit_predict(X)

        #print silhouette_score(X, cluster_labels)

        # aggregate cluster labels to players in that cluster
        player_clusters = {}
        for p, c in zip(pids, cluster_labels):
            cluster = player_clusters.get(c, [])
            cluster.append(p)
            player_clusters[c] = cluster

        # generate clustered regressors
        fc = self.feature_creator

        r2_score_clustered = {}
        
        for cid, player_ids in player_clusters.iteritems():
            r2_score = {}

            # fit on that
            sf = fc.get_some_training_features(player_ids)
            for fid in self.STAT_FEATURES:
                r2_score[fid] = self.fit_feature(fid, sf)

            ff = fc.get_some_training_fanduel(player_ids)
            for fid in self.FD_FEATURES:
                r2_score[fid] = self.fit_feature(fid, ff)

            r2_score_clustered[cid] = r2_score
            self.feature_regressors_clustered[cid] = \
                self.feature_regressors

        return r2_score_clustered

    def get_player_cluster(self, player_id):
        x_cluster = \
            self.feature_creator.get_player_average_fanduel(player_id)
        x_cluster = np.array([[x_cluster]])
        cid = self.clusterer.predict(x_cluster)[0]
        return cid

    def get_stat_projection(self, player_id):
        cid = self.get_player_cluster(player_id)
        self.feature_regressors = \
            self.feature_regressors_clustered[cid]

        return (super(ClusteringFeatureProjector, self)
                    .get_stat_projection(player_id))

    def get_fanduel_projection(self, player_id):
        cid = self.get_player_cluster(player_id)
        self.feature_regressors = \
            self.feature_regressors_clustered[cid]

        return (super(ClusteringFeatureProjector, self)
                    .get_fanduel_projection(player_id))

class LRFeatureProjector(FeatureProjector):
    def __init__(self, feature_creator):
        super(self.__class__, self).__init__(
            feature_creator,
            self.__get_regression_object)

    def __get_regression_object(self):
        return LinearRegression()

class LassoFeatureProjector(FeatureProjector):
    def __init__(self, feature_creator):
        super(self.__class__, self).__init__(
            feature_creator,
            self.__get_regression_object)

    def __get_regression_object(self):
        return Lasso(alpha=0.1)

class RFRFeatureProjector(FeatureProjector):
    def __init__(self, feature_creator):
        super(self.__class__, self).__init__(
            feature_creator,
            self.__get_regression_object)

    def __get_regression_object(self):
        return RandomForestRegressor(n_estimators=100, n_jobs=-1,
                                     max_features='sqrt')

class SVRLinearFeatureProjector(ClusteringFeatureProjector):
    def __init__(self, feature_creator, n_clusters=3):
        super(self.__class__, self).__init__(
            feature_creator,
            self.__get_regression_object,
            n_clusters)

    def __get_regression_object(self):
        return SVR(kernel='linear', C=1.)

class SVRRBFFeatureProjector(ClusteringFeatureProjector):
    def __init__(self, feature_creator, n_clusters=3):
        super(self.__class__, self).__init__(
            feature_creator,
            self.__get_regression_object,
            n_clusters)

    def __get_regression_object(self):
        return SVR(kernel='rbf', C=1.)

class DailyProjector(object):
    # store upcoming games details
    upcoming_games = {}
    # store all players details
    players = {}

    def prepare_data_for_projections(self, text_file=None):
        if text_file:
            with open(text_file, 'r') as inf:
                for line in inf:
                    nf_data = eval(line)
        else:
            nf_data = nf_scraper.get_todays_player_data()

        csv_helper = CSVHelper()
        self.players, nf_to_stattleship_map = \
            csv_helper.prepare_data_from_csvs()

        for nf_id, attributes in nf_data.iteritems():
            stattleship_slug = nf_to_stattleship_map[nf_id]
            self.upcoming_games[stattleship_slug] = dict()
            for attr in attributes:
                self.upcoming_games[stattleship_slug][attr] = \
                    nf_data[nf_id][attr]

        for player_id in deepcopy(self.players.keys()):
            if player_id not in self.upcoming_games.keys():
                pass #del(self.players[player_id])
            else:
                self.players[player_id]['position'] = \
                    set(self.upcoming_games[player_id]['position'])

    def project_fd_score(self):
        fc = FeatureCreator(self.players, self.upcoming_games)

        players_projected = []

        print "\nLinear Regression"
        proj = LRFeatureProjector(fc)
        print "r2 score"
        print proj.fit_all()
        for pid in self.upcoming_games.keys():
            print "Projecting for", pid
            print "stats"
            projections = proj.get_stat_projection(pid)
            print projections
            stats_fanduel = proj.get_fanduel_score(projections)
            print "stats: fanduel", stats_fanduel
            #print "fanduel"
            #projections = LRproj.get_fanduel_projection(pid)
            #print projections
            print "\n------------------------"

            players_projected.append({
                'position': self.upcoming_games[pid]['position'],
                'name': self.players[pid]['name'],
                'salary': self.upcoming_games[pid]['salary'],
                'projection': stats_fanduel
                })

        return players_projected
