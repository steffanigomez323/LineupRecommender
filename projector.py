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
from sklearn.svm import SVR
from sklearn.cross_validation import train_test_split
from collections import Counter
from scorer import FanDuelScorer
import numpy as np
from app import redis_db
from app import namespace


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

class FeatureProjector(object):

    POINTS_IDX = 11;
    REBOUNDS_IDX = 6;
    ASSISTS_IDX = 7;
    STEALS_IDX = 8;
    BLOCKS_IDX = 9;
    TURNOVERS_IDX = 10;
    TIME_IDX = 1;
    OPPONENT_IDX = 3;
    HVA_IDX = 2;
    PLUS_MINUS_IDX = 4;

    # take in pos, height, gamelogs
    # {id: {position: ssfd, height:fasdf}}
    def __init__(self, players_gamelogs, players_stats):
        self.avg = lambda x: sum(x) / float(len(x))

        self.players_gamelogs = players_gamelogs['allgames']
        self.players_stats = players_stats

    def get_projection(self, player_id):
        pass

    def get_player_training_features(self, player_id):
        player = players_stats[player_id]

        position = player['position']
        height = player['height']

        gamelog = players_gamelogs[player_id]['allgames']

        points = gamelog[:,self.POINTS_IDX]
        rebounds = gamelog[:,self.REBOUNDS_IDX]
        assists = gamelog[:,self.ASSISTS_IDX]
        steals = gamelog[:,self.STEALS_IDX]
        blocks = gamelog[:,self.BLOCKS_IDX]
        turnovers = gamelog[:,self.TURNOVERS_IDX]
        time = gamelog[:,self.TIME_IDX]
        opponent = gamelog[:,self.OPPONENT_IDX]
        hva = gamelog[:,self.HVA_IDX]
        plus_minus = gamelog[:,self.PLUS_MINUS_IDX]

        num_logs = len(points)

        # points
        points_train = np.array([])
        for i in range(7, num_logs):
            row = [points[i], # label
                   self.avg(points[i-1:i]), # last 1
                   self.avg(points[i-3:i]), # last 3
                   self.avg(points[i-5:i]), # last 5
                   self.avg(points[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            row = np.array(row)
            points_train.append(row)

        # assists
        assists_train = np.array([])
        for i in range(7, num_logs):
            row = [assists[i], # label
                   self.avg(assists[i-1:i]), # last 1
                   self.avg(assists[i-3:i]), # last 3
                   self.avg(assists[i-5:i]), # last 5
                   self.avg(assists[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            row = np.array(row)
            assists_train.append(row)

        # steals
        steals_train = np.array([])
        for i in range(7, num_logs):
            row = [steals[i], # label
                   self.avg(steals[i-1:i]), # last 1
                   self.avg(steals[i-3:i]), # last 3
                   self.avg(steals[i-5:i]), # last 5
                   self.avg(steals[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            row = np.array(row)
            steals_train.append(row)

        # turnovers
        turnovers_train = np.array([])
        for i in range(7, num_logs):
            row = [turnovers[i], # labels
                   self.avg(turnovers[i-1:i]), # last 1
                   self.avg(turnovers[i-3:i]), # last 3
                   self.avg(turnovers[i-5:i]), # last 5
                   self.avg(turnovers[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position] # pos
            row = np.array(row)
            turnovers_train.append(row)

        # rebounds
        rebounds_train = np.array([])
        for i in range(7, num_logs):
            row = [rebounds[i], # label
                   self.avg(rebounds[i-1:i]), # last 1
                   self.avg(rebounds[i-3:i]), # last 3
                   self.avg(rebounds[i-5:i]), # last 5
                   self.avg(rebounds[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position, # pos
                   height] # height
            row = np.array(row)
            rebounds_train.append(row)

        # blocks
        blocks_train = np.array([])
        for i in range(7, num_logs):
            row = [blocks[i], # label
                   self.avg(blocks[i-1:i]), # last 1
                   self.avg(blocks[i-3:i]), # last 3
                   self.avg(blocks[i-5:i]), # last 5
                   self.avg(blocks[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent[i], # opponent
                   hva[i], # home v away
                   position, # pos
                   height] # height
            row = np.array(row)
            blocks_train.append(row)

        return {"assists": assists_train,
                "points": points_train,
                "blocks": blocks_train,
                "rebounds": rebounds_train,
                "turnovers": turnovers_train,
                "steals": steals_train}

    def get_player_projection_features(self, player_id):
        player = players_stats[player_id]

        position = player['position']
        height = player['height']

        gamelog = players_gamelogs[player_id]

        opponent = safdsa
        hva = afdsa

        points = gamelog[:,self.POINTS_IDX]
        rebounds = gamelog[:,self.REBOUNDS_IDX]
        assists = gamelog[:,self.ASSISTS_IDX]
        steals = gamelog[:,self.STEALS_IDX]
        blocks = gamelog[:,self.BLOCKS_IDX]
        turnovers = gamelog[:,self.TURNOVERS_IDX]
        time = gamelog[:,self.TIME_IDX]
        plus_minus = gamelog[:,self.PLUS_MINUS_IDX]

        num_logs = len(points)
        i = num_logs

        # points
        points_proj = [self.avg(points[i-1:i]), # last 1
                       self.avg(points[i-3:i]), # last 3
                       self.avg(points[i-5:i]), # last 5
                       self.avg(points[i-7:i]), # last 7
                       self.avg(plus_minus[0:i-1]), # plus minus avg
                       self.avg(time[0:i-1]), # time avg
                       opponent, # opponent
                       hva, # home v away
                       position] # pos

        # assists
        assists_proj = [self.avg(assists[i-1:i]), # last 1
                        self.avg(assists[i-3:i]), # last 3
                        self.avg(assists[i-5:i]), # last 5
                        self.avg(assists[i-7:i]), # last 7
                        self.avg(plus_minus[0:i-1]), # plus minus avg
                        self.avg(time[0:i-1]), # time avg
                        opponent, # opponent
                        hva, # home v away
                        position] # pos

        # steals
        steals_proj = [self.avg(steals[i-1:i]), # last 1
                       self.avg(steals[i-3:i]), # last 3
                       self.avg(steals[i-5:i]), # last 5
                       self.avg(steals[i-7:i]), # last 7
                       self.avg(plus_minus[0:i-1]), # plus minus avg
                       self.avg(time[0:i-1]), # time avg
                       opponent, # opponent
                       hva, # home v away
                       position] # pos

        # turnovers
        turnovers_proj = [self.avg(turnovers[i-1:i]), # last 1
                          self.avg(turnovers[i-3:i]), # last 3
                          self.avg(turnovers[i-5:i]), # last 5
                          self.avg(turnovers[i-7:i]), # last 7
                          self.avg(plus_minus[0:i-1]), # plus minus avg
                          self.avg(time[0:i-1]), # time avg
                          opponent, # opponent
                          hva, # home v away
                          position] # pos

        # rebounds
        rebounds_proj = [self.avg(rebounds[i-1:i]), # last 1
                   self.avg(rebounds[i-3:i]), # last 3
                   self.avg(rebounds[i-5:i]), # last 5
                   self.avg(rebounds[i-7:i]), # last 7
                   self.avg(plus_minus[0:i-1]), # plus minus avg
                   self.avg(time[0:i-1]), # time avg
                   opponent, # opponent
                   hva, # home v away
                   position, # pos
                   height] # height

        # blocks
        blocks_proj = [self.avg(blocks[i-1:i]), # last 1
                       self.avg(blocks[i-3:i]), # last 3
                       self.avg(blocks[i-5:i]), # last 5
                       self.avg(blocks[i-7:i]), # last 7
                       self.avg(plus_minus[0:i-1]), # plus minus avg
                       self.avg(time[0:i-1]), # time avg
                       opponent, # opponent
                       hva, # home v away
                       position, # pos
                       height] # height

        return {"assists": assists_proj,
                "points": points_proj,
                "blocks": blocks_proj,
                "rebounds": rebounds_proj,
                "turnovers": turnovers_proj,
                "steals": steals_proj}

    def split_train_xy(self, training_feature):
        y, X = np.hsplit( # split off first column (labels)
            training_feature,
            [0])

        return X, y

    def split_train_test(self, training_feature, test_percent):
        X, y = self.split_train_xy(training_feature)

        return train_test_split(
            X, y,
            test_size=test_percent, random_state=42)

class SvrFeatureProjector(FeatureProjector):
    def __project_feature(self, feature_id, features, projections):
        x_train, x_test, \
        y_train, y_test = self.split_train_test(
            features[feature_id], 0.25)

        svr = SVR(kernel='rbf', C=.5).fit(
            x_train, y_train)

        score = svr.score(x_test, y_test)
        proj = svr.predict(projections[feature_id])

        return proj, score

    def get_projection(self, player_id):
        features = self.get_player_training_features(player_id)
        projections = self.get_player_projection_features(player_id)

        ast_proj, ast_score = self.__project_feature('assists', features, projections)

        blk_proj, blk_score = self.__project_feature('blocks', features, projections)

        stl_proj, stl_score = self.__project_feature('steals', features, projections)

        pts_proj, pts_score = self.__project_feature('points', features, projections)

        reb_proj, reb_score = self.__project_feature('rebounds', features, projections)

        tov_proj, tov_score = self.__project_feature('turnovers', features, projections)

        return {"assists": (ast_proj, ast_score),
                "points": (pts_proj, pts_score),
                "blocks": (blk_proj, blk_score),
                "rebounds": (reb_proj, reb_score),
                "turnovers": (tov_proj, tov_score),
                "steals": (stl_proj, stl_score)}

class DailyProjector(object):
    def get_player_stats(self, nf_ids):
      player_stats = {}
      for nf in nf_ids:
        nba_id = redis_db.get(nf)
        stattleship_slug = redis_db.get(nba_id)
        height = redis_db.hget(stattleship_slug, 'height')
        position = redis_db.hget(stattleship_slug, 'position')
        stats = { 'height': height, 'position': position }
        player_stats[nf] = stats
      return player_stats

    def get_player_gamelogs(self, nf_ids):
      gamelogs = {}
      for nf in nf_ids:
        nba_id = redis_db.get(nf)
        stattleship_slug = redis_db.get(nba_id)
        gameids = redis_db.lrange(stattleship_slug + namespace.GAMELOGS, 0, -1)
        games = []
        for game in gameids:
          g = [game]
          g.append(redis_db.hget(game, 'game_time'))
          g.append(redis_db.hget(game, 'played_at_home'))
          g.append(redis_db.hget(game, 'played_against'))
          g.append(redis_db.hget(game, 'plus_minus'))
          g.append(redis_db.hget(game, 'time_played_total'))
          g.append(redis_db.hget(game, 'rebounds_total'))
          g.append(redis_db.hget(game, 'assists'))
          g.append(redis_db.hget(game, 'steals'))
          g.append(redis_db.hget(game, 'blocks'))
          g.append(redis_db.hget(game, 'turnovers'))
          g.append(redis_db.hget(game, 'points'))
          game.append(np.array(g))
        gamelogs[nf] = np.array(games)
      return gamelogs
