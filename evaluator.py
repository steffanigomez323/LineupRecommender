"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Evaluator

http://lesswrong.com/lw/k2a/the_usefulness_of_forecasts_and_the_rationality/
"""

# from scorer import FanDuelScorer
from sklearn.metrics import mean_squared_error


class Evaluator(object):
    def __init__(self, scorer):
        self.__scorer = scorer

    def find_actual_scores(actual_gamelogs):
        return [self.__scorer.find_game_score(g)["SCORE"]
                for g in actual_gamelogs]

    def find_projection_error(self, proj_score, actual_score):
        predicted = proj_score
        actual = actual_score
        return predicted - actual

    def find_projection_performance(self, proj_scores, actual_scores):
        mse = mean_squared_error(actual_scores, proj_scores)
        msd = reduce(lambda x,y: x + find_projection_error(y[0], y[1]),
                     zip(proj_scores, actual_scores),
                     0)
        return {"MEAN SQUARED ERROR": mse,
                "MEAN SIGNED DEVIATION": msd}
'''
    def compare_lineup_projection(self, proj_lineups, actual_lineups):
        predicted = reduce(lambda x,y: x + self.__scorer.find_game_score(y),
                           proj_lineups,
                           0)
        actual = reduce(lambda x,y: x + self.__scorer.find_game_score(y),
                        actual_lineups,
                        0)
        return {"PREDICTED": predicted,
                "ACTUAL": actual,
                "ERROR": predicted - actual,
                "PERCENT_ERROR": (predicted - actual) / actual}
'''

'''
class FanDuelEvaluator(Evaluator):
    def __init__(self):
            super(FanDuelEvaluator, self).__init__(FanDuelScorer())
'''
