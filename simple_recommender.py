"""
CS1951A Final Project
Brown University
Spring 2015

Vann, Steffani, JJ, Chaitu

Simple Optimal Lineup Recommender
"""


class SimpleRecommender(object):
    salary_cap = 60000
    lineup_size = 9

    def __init__(self, players):
        self.players = players

    def print_all_players(self):
        for player in self.players:
            print player
