"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Scorers
"""

class Scorer(object):
    def __init__(self, scorer_op):
        self.__scorer_op = scorer_op

    def find_game_score(self, game):
        return {'DATE': game['DATE'],
                'SCORE': self.__scorer_op(game)}

    def find_player_scores(self, player):
        return {'PLAYER_NAME': player['PLAYER_NAME'],
                'TEAM_NAME': player['TEAM_NAME'],
                'GAME_SCORES': [self.find_game_score(g) for g in player['GAMES']]}

    def score_all_players(self, players_dict):
        return {k: self.find_player_scores(v) for k, v in players_dict.items()}

"""
This class is used to find the fanduel score from the fanduel formula, where each statistic is the projected statistic.
"""

class FanDuelScorer(Scorer):
    FG3 = 3
    FG2 = 2
    FrT = 1
    REB = 1.2
    AST = 1.5
    BLK = 2
    STL = 2
    TOV = -1

    @staticmethod
    def find_fanduel_score(game):
        score = (FanDuelScorer.FG3 * game['3PT_FG'] +
                 FanDuelScorer.FG2 * game['2PT_FG'] +
                 FanDuelScorer.FrT * game['FT'] +
                 FanDuelScorer.REB * game['REB'] +
                 FanDuelScorer.AST * game['AST'] +
                 FanDuelScorer.BLK * game['BLK'] +
                 FanDuelScorer.STL * game['STL'] +
                 FanDuelScorer.TOV * game['TOV'])
        return round(score, 1)

    def __init__(self):
        super(FanDuelScorer, self).__init__(self.find_fanduel_score)
