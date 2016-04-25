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


class PlayerProjector(object):
    def __init__(self, player_stats, player_gamelogs, avg_gamelogs):
        self.p_height = player_stats['']
        self.p_weight = player_stats['']
        self.p_experience = player_stats['']

        self.g_steals = player_gamelogs['']
        self.g_assists = player_gamelogs['']
        self.g_rebounds = player_gamelogs['']
        self.g_points = player_gamelogs['']
        self.g_turnovers = player_gamelogs['']
        self.g_blocks = player_gamelogs['']
        self.g_minutes = player_gamelogs['']
        self.g_plus_minus = player_gamelogs['']
        self.g_hva = player_gamelogs['']
        self.g_opponent = player_gamelogs['']

        self.a_steals = avg_gamelogs['']
        self.a_assists = avg_gamelogs['']
        self.a_rebounds = avg_gamelogs['']
        self.a_points = avg_gamelogs['']
        self.a_turnovers = avg_gamelogs['']
        self.a_blocks = avg_gamelogs['']
        self.a_minutes = avg_gamelogs['']

    def get_projection(self, last_n):
        stl = self.project_steals(last_n)
        ast = self.project_assists(last_n)
        reb = self.project_rebounds(last_n)
        tov = self.project_turnovers(last_n)
        blk = self.project_blocks(last_n)

        game = {}
        game['3PT_FG'] = 
        game['2PT_FG'] = 
        game['FT'] = 
        game['REB'] = reb
        game['AST'] = ast
        game['BLK'] = blk
        game['STL'] = stl
        game['TOV'] = tov
        return FanDuelScorer.get_score(game)

    def project_steals(self, last_n):
    
    def project_assists(self, last_n):

    def project_rebounds(self, last_n):

    def project_turnovers(self, last_n):

    def project_blocks(self, last_n):