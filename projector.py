"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Player Performance Projector
"""


import operator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from collections import Counter
from scorer import FanDuelScorer
import numpy


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
                    last_n_dict[player][i][1].append(self.avg(scores[j-i:j]))
        return last_n_dict

    def get_best_last_n(self, last_n_dict, num_games):
        r2_dict = {}
        for player in last_n_dict.iterkeys():
            r2_dict[player] = {}    
            for last_n in last_n_dict[player].iterkeys():
                if len(last_n_dict[player][last_n][0]) > 0:
                    assert len(last_n_dict[player][last_n][0]) == len(last_n_dict[player][last_n][1])
                    r2_dict[player][last_n] = r2_score(last_n_dict[player][last_n][0], last_n_dict[player][last_n][1])

        count_14s = 0
        last_ns = []
        for player, last_n in r2_dict.iteritems():
            if len(last_n) == num_games - 1:
                count_14s += 1
                last_ns.append(max(last_n.iteritems(), key=operator.itemgetter(1))[0])

        data = Counter(last_ns)
        return data.most_common(1)[0][0]

    def get_projection(self, scores, averages, last_n):
        classifier = LogisticRegression()
        #print "#### SCORES"
        #print scores
        #print "#### AVERAGES"
        #print averages
        classifier.fit(numpy.array([numpy.array([average]) for average in averages]), numpy.array([int(score) for score in scores]))
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
        player_features = {k: v[feature_id] for k,v in self.players.items()}

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

class SGRProjector(object):
    def __init__(self, players):
        self.players = players
        self.avg = lambda x: sum(x) / float(len(x))

    def get_player_features(self, player_id):
        player = players[player_id]

        num_logs = len(player['opponent'])
        position = player['position']
        height = player['height']

        points = player['points']
        rebounds = player['rebounds']
        assists = player['assists']
        steals = player['steals']
        blocks = player['blocks']
        time = player['time']
        opponent = player['opponent']
        hva = player['hva']
        plus_minus = player['plus_minus']

        # points
        points_x_train = []
        points_y_train = list(points[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(points[i-1:i]), # last 1
                   self.avg(points[i-3:i]), # last 3
                   self.avg(points[i-5:i]), # last 5
                   self.avg(points[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            points_x_train.append(row)

        # assists
        assists_x_train = []
        assists_y_train = list(assists[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(assists[i-1:i]), # last 1
                   self.avg(assists[i-3:i]), # last 3
                   self.avg(assists[i-5:i]), # last 5
                   self.avg(assists[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            points_x_train.append(row)

        # steals
        steals_x_train = []
        steals_y_train = list(steals[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(steals[i-1:i]), # last 1
                   self.avg(steals[i-3:i]), # last 3
                   self.avg(steals[i-5:i]), # last 5
                   self.avg(steals[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            steals_x_train.append(row)

        # turnovers
        turnovers_x_train = []
        turnovers_y_train = list(turnovers[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(turnovers[i-1:i]), # last 1
                   self.avg(turnovers[i-3:i]), # last 3
                   self.avg(turnovers[i-5:i]), # last 5
                   self.avg(turnovers[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            turnovers_x_train.append(row)

        # rebounds
        rebounds_x_train = []
        rebounds_y_train = list(rebounds[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(rebounds[i-1:i]), # last 1
                   self.avg(rebounds[i-3:i]), # last 3
                   self.avg(rebounds[i-5:i]), # last 5
                   self.avg(rebounds[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position, # pos
                   height] # height
            rebounds_x_train.append(row)

        # rebounds
        blocks_x_train = []
        blocks_y_train = list(blocks[8:num_logs])
        for i in range(7, num_logs-1):
            row = [self.avg(blocks[i-1:i]), # last 1
                   self.avg(blocks[i-3:i]), # last 3
                   self.avg(blocks[i-5:i]), # last 5
                   self.avg(blocks[i-7:i]), # last 7
                   self.avg(plus_minus[0:i]), # plus minus avg
                   self.avg(time[0:i]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position, # pos
                   height] # height
            blocks_x_train.append(row)

        return


'''
class PlayerProjector(object):
    def __init__(self, player_gamelogs):
        self.p_logs = player_gamelogs

        self.avg_logs = self.calc_average_gamelogs()

    def get_projection(self, player_id):
        pts = self.project_points(player_id)
        stl = self.project_steals(player_id)
        ast = self.project_assists(player_id)
        reb = self.project_rebounds(player_id)
        tov = self.project_turnovers(player_id)
        blk = self.project_blocks(lplayer_id)

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

    def project_steals(self, last_n):
        return 0
    
    def project_assists(self, last_n):
        return 0

    def project_rebounds(self, last_n):
        return 0

    def project_turnovers(self, last_n):
        return 0

    def project_blocks(self, last_n):
        return 0
'''
