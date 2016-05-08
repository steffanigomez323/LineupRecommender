"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Player Performance Projector
"""


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
import operator
from collections import Counter
from scorer import FanDuelScorer
import numpy as np
from copy import deepcopy
from app import nf_scraper
from db_helper import CSVHelper
from namespace import Namespace


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


class FeatureProjector(object):
    POINTS_IDX = 10
    REBOUNDS_IDX = 5
    ASSISTS_IDX = 6
    STEALS_IDX = 7
    BLOCKS_IDX = 8
    TURNOVERS_IDX = 9
    TIME_IDX = 4
    OPPONENT_IDX = 2
    HVA_IDX = 1
    PLUS_MINUS_IDX = 3

    OPPONENT_LIST = [x for x in Namespace.TEAM_MAP_NF_NBA.itervalues()]
    OPPONENT_LIST.pop()
    POSITION_LIST = [x for x in Namespace.POSITIONS]
    POSITION_LIST.pop()

    TRUE_NUM = 1
    FALSE_NUM = 0

    SCORER = lambda x: x['points'] + x['rebounds']*1.2 + x['assists']*1.5 +
        x['blocks']*2 + x['steals']*2 - x['turnovers']

    # take in pos, height, gamelogs
    # {id: {position: ssfd, height:fasdf}}
    def __init__(self, players_gamelogs, upcoming_games):
        self.avg = lambda x: sum(x) / float(len(x))

        self.players_gamelogs = players_gamelogs
        self.upcoming_games = upcoming_games

    def get_projection(self, player_id):
        pass

    def __append_features(self, target, append_array):
        if target == None:
            return append_array
        else:
            return np.vstack((target, append_array))

    def get_all_training_features(self):
        all_features = {"assists": None,
                        "points": None,
                        "blocks": None,
                        "rebounds": None,
                        "turnovers": None,
                        "steals": None}

        for pid in self.players_gamelogs.iterkeys():
            features = self.get_player_training_features(pid)

            for k, v in features.iteritems():
                all_features[k] = self.__append_features(all_features[k], v)

        return all_features

    def get_player_training_features(self, player_id):
        # position = self.players_gamelogs[player_id]['position']
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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

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
            # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
            #                 for x in self.POSITION_LIST]
            row.append(hva_num)  # hva
            row.extend(opponent_nums)  # opponent
            # row.extend(position_nums) # position

            blocks_train.append(row)

        return {"assists": np.array(assists_train),
                "points": np.array(points_train),
                "blocks": np.array(blocks_train),
                "rebounds": np.array(rebounds_train),
                "turnovers": np.array(turnovers_train),
                "steals": np.array(steals_train)}

    def get_player_projection_features(self, player_id):
        # position = self.players_gamelogs[player_id]['position']
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
        # position_nums = [self.TRUE_NUM if x == position else self.FALSE_NUM
        #                 for x in self.POSITION_LIST]

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
        # points_proj.extend(position_nums)

        # assists
        assists_proj = [self.avg(assists[i - 1:i]),  # last 1
                        self.avg(assists[i - 3:i]),  # last 3
                        self.avg(assists[i - 5:i]),  # last 5
                        self.avg(assists[i - 7:i]),  # last 7
                        self.avg(plus_minus[0:i]),  # plus minus avg
                        self.avg(time[0:i])]  # time avg
        assists_proj.append(hva_num)
        assists_proj.extend(opponent_nums)
        # assists_proj.extend(position_nums)

        # steals
        steals_proj = [self.avg(steals[i - 1:i]),  # last 1
                       self.avg(steals[i - 3:i]),  # last 3
                       self.avg(steals[i - 5:i]),  # last 5
                       self.avg(steals[i - 7:i]),  # last 7
                       self.avg(plus_minus[0:i]),  # plus minus avg
                       self.avg(time[0:i])]  # time avg
        steals_proj.append(hva_num)
        steals_proj.extend(opponent_nums)
        # steals_proj.extend(position_nums)

        # turnovers
        turnovers_proj = [self.avg(turnovers[i - 1:i]),  # last 1
                          self.avg(turnovers[i - 3:i]),  # last 3
                          self.avg(turnovers[i - 5:i]),  # last 5
                          self.avg(turnovers[i - 7:i]),  # last 7
                          self.avg(plus_minus[0:i]),  # plus minus avg
                          self.avg(time[0:i])]  # time avg
        turnovers_proj.append(hva_num)
        turnovers_proj.extend(opponent_nums)
        # turnovers_proj.extend(position_nums)

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
        # rebounds_proj.extend(position_nums)

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
        # blocks_proj.extend(position_nums)

        return {"assists": np.array(assists_proj).reshape(1, -1),
                "points": np.array(points_proj).reshape(1, -1),
                "blocks": np.array(blocks_proj).reshape(1, -1),
                "rebounds": np.array(rebounds_proj).reshape(1, -1),
                "turnovers": np.array(turnovers_proj).reshape(1, -1),
                "steals": np.array(steals_proj).reshape(1, -1)}

    def split_train_xy(self, training_feature):
        y, X = np.hsplit(  # split off first column (labels)
            training_feature,
            [1])

        return X, np.ravel(y)

    def split_train_test(self, training_feature, test_percent):
        X, y = self.split_train_xy(training_feature)

        return train_test_split(
            X, y,
            test_size=test_percent, random_state=42)


class LRFeatureProjector(FeatureProjector):

    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, y_train, y_test = \
            self.split_train_test(features[feature_id], 0.25)

        lr = LinearRegression().fit(x_train, y_train)

        score = lr.score(x_test, y_test)
        proj = lr.predict(projections[feature_id])

        # print lr.coef_

        return proj, score

    def get_stat_projections(self, player_id):
        features = self.get_all_training_features()
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features,
                                                     projections)

        blk_proj, blk_score = self.__project_feature('blocks', features,
                                                     projections)

        stl_proj, stl_score = self.__project_feature('steals', features,
                                                     projections)

        pts_proj, pts_score = self.__project_feature('points', features,
                                                     projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features,
                                                     projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features,
                                                     projections)
        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}

    def get_fanduel_score(self, stats_projections):

        pass

    def get_fanduel_projection(self):
        pass


class LassoFeatureProjector(FeatureProjector):

    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, y_train, y_test = \
            self.split_train_test(features[feature_id], 0.25)

        lr = Lasso(alpha=0.1).fit(x_train, y_train)

        score = lr.score(x_test, y_test)
        proj = lr.predict(projections[feature_id])

        return proj, score

    def get_stat_projections(self, player_id):
        features = self.get_all_training_features()
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features,
                                                     projections)

        blk_proj, blk_score = self.__project_feature('blocks', features,
                                                     projections)

        stl_proj, stl_score = self.__project_feature('steals', features,
                                                     projections)

        pts_proj, pts_score = self.__project_feature('points', features,
                                                     projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features,
                                                     projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features,
                                                     projections)
        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}


class RFRFeatureProjector(FeatureProjector):

    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, y_train, y_test = \
            self.split_train_test(features[feature_id], 0.25)

        rf = RandomForestRegressor(n_estimators=1000, n_jobs=-1,
                                   max_features='sqrt').fit(x_train, y_train)

        score = rf.score(x_test, y_test)
        proj = rf.predict(projections[feature_id])

        return proj, score

    def get_stat_projections(self, player_id):
        features = self.get_all_training_features()
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features,
                                                     projections)

        blk_proj, blk_score = self.__project_feature('blocks', features,
                                                     projections)

        stl_proj, stl_score = self.__project_feature('steals', features,
                                                     projections)

        pts_proj, pts_score = self.__project_feature('points', features,
                                                     projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features,
                                                     projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features,
                                                     projections)
        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}


class SVRLinearFeatureProjector(FeatureProjector):

    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, y_train, y_test = \
            self.split_train_test(features[feature_id], 0.25)

        svr = SVR(kernel='linear', C=.5).fit(
            x_train, y_train)

        score = svr.score(x_test, y_test)
        proj = svr.predict(projections[feature_id])

        return proj, score

    def get_stat_projections(self, player_id):
        features = self.get_all_training_features()
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features,
                                                     projections)

        blk_proj, blk_score = self.__project_feature('blocks', features,
                                                     projections)

        stl_proj, stl_score = self.__project_feature('steals', features,
                                                     projections)

        pts_proj, pts_score = self.__project_feature('points', features,
                                                     projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features,
                                                     projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features,
                                                     projections)
        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}


class SVRRBFFeatureProjector(FeatureProjector):

    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, y_train, y_test = \
            self.split_train_test(features[feature_id], 0.25)

        svr = SVR(kernel='rbf', C=.5).fit(
            x_train, y_train)

        score = svr.score(x_test, y_test)
        proj = svr.predict(projections[feature_id])

        return proj, score

    def get_projection(self, player_id):
        features = self.get_all_training_features()
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features,
                                                     projections)

        blk_proj, blk_score = self.__project_feature('blocks', features,
                                                     projections)

        stl_proj, stl_score = self.__project_feature('steals', features,
                                                     projections)

        pts_proj, pts_score = self.__project_feature('points', features,
                                                     projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features,
                                                     projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features,
                                                     projections)

        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}


class DailyProjector(object):
    # store upcoming games details
    upcoming_games = {}
    # store all players details
    players = {}

    def prepare_data_for_projections(self):
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
                del(self.players[player_id])
            else:
                self.players[player_id]['position'] = \
                    self.upcoming_games[player_id]['position']

    def project_fd_score(self):
        pid = 'nba-lebron-james'

        print "Projecting for", pid

        print "\nLinear Regression"
        proj = LRFeatureProjector(self.players, self.upcoming_games)
        projections = proj.get_projection(pid)
        print projections

        print "\nLasso Regression"
        proj = LassoFeatureProjector(self.players, self.upcoming_games)
        projections = proj.get_projection(pid)
        print projections

        print "\nRFR Regression"
        proj = RFRFeatureProjector(self.players, self.upcoming_games)
        projections = proj.get_projection(pid)
        print projections

        print "\nSVR (Linear) Regression"
        proj = SVRLinearFeatureProjector(self.players, self.upcoming_games)
        projections = proj.get_projection(pid)
        print projections

        print "\nSVR (RBF) Regression"
        proj = SVRRBFFeatureProjector(self.players, self.upcoming_games)
        projections = proj.get_projection(pid)
        print projections
