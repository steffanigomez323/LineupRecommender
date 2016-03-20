"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Simple Optimal Lineup Recommender
"""
import random

class SimpleRecommender(object):
    salary_cap = 60000
    lineup_size = 9

    def __init__(self, players):
        self.players = players

    def print_all_players(self):
        for player in self.players:
            print player
    
    """
    This is a method returns a simple, optimal lineup based on the salaries from swish analytics.
    """

    def get_simple_lineup(self):
        lineup = list()
        salary = 0
        pg = 0
        sg = 0
        sf = 0
        pf = 0
        c = 0
        
        playersSorted = sorted(self.players, key=lambda x: float(x.projected_points), reverse=True)

        for p in playersSorted:
            if p.injury_status == "Not Injured" and int(p.salary) <= (self.salary_cap / 9):
                if p.position == 'PG':                     
                    if p not in lineup:
                        if (pg <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            pg = pg + 1

                elif p.position == 'SG':
                    if p not in lineup:
                        if (sg <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            sg = sg + 1
                            
                elif p.position == 'SF':
                    if p not in lineup:
                        if (sf <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            sf = sf + 1

                elif p.position == 'PF':
                    if p not in lineup:
                        if (pf <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            pf = pf + 1
                            
                else: # the position is C (Center)
                    if p not in lineup:
                        if (c <= 0):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            c = c + 1
                            
            if c > 0 and pf > 1 and sf > 1 and sg > 1 and pg > 1:
                break
                               
        assert(len(lineup) == 9)
        assert(salary <= self.salary_cap)

        return lineup
                     