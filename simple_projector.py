"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Simple Optimal Lineup Recommender
"""


import random
import numpy
from sklearn.linear_model import LogisticRegression

class SimpleProjector(object):
    def __init__(self, players):
        self.players = players

    def print_all_players(self):
        for player in self.players:
            print player

    """
    This is a method returns a dictionary from player name to projected score for the next game.
    """
    def get_simple_projections(self):
        avg = lambda x: sum(x) / float(len(x))
        scores = self.players['Lebron James']
        last_n_dict = {}
        for i in range(1, 6):
            last_n_dict[i] = [[], []]
            for j in range(i, len(scores)):
                last_n_dict[i][0].append(scores[j])
                last_n_dict[i][1].append(avg(scores[j-i:j]))
        

