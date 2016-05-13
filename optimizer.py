"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Optimal Lineup Recommender
"""


from openopt import *


class LineupOptimizer(object):

    def __init__(self, players, budget=60000, solver="glpk"):
        self.players = players
        self.player_sack = self.load_players_into_sack()
        self.budget = budget
        self.solver = solver

    def load_players_into_sack(self):
        player_sack = list()

        num_ids = 0
        check_position = lambda x, y: 1 if x == y else 0

        for name in self.players.iterkeys():
            num_ids += 1

            position = self.players[name]['position']
            salary = self.players[name]['salary']
            score = self.players[name]['projection']

            player_sack.append({"player_id": num_ids,
                                "name": name,
                                "small_forward": check_position(
                                    "SF", position),
                                "power_forward": check_position(
                                    "PF", position),
                                "shooting_guard": check_position(
                                    "SG", position),
                                "point_guard": check_position(
                                    "PG", position),
                                "center": check_position("C", position),
                                "salary": int(salary),
                                "score": score})

        all_ids = range(num_ids + 1)

        for player in player_sack:
            for i in all_ids:
                player['id' + str(i)] = float(player['player_id'] == i)

        return player_sack

    def optimize(self):
        all_ids = range(self.player_sack[-1]['player_id'] + 1)

        constraints = lambda values: (
            # salary cap constraint
            values['salary'] <= self.budget,

            # position constraints
            values['small_forward'] == 2,
            values['power_forward'] == 2,
            values['point_guard'] == 2,
            values['shooting_guard'] == 2,
            values['center'] == 1

            # add constraints to restrict number of each player to 1
        ) + tuple([values['id' + str(i)] <= 1 for i in all_ids])

        objective = 'score'

        ksp = KSP(objective, self.player_sack, constraints=constraints)
        r = ksp.solve(self.solver, iprint=1, nProc=2)

        return [self.players[name] for name in r.xf]


"""

        update = []
        lineup = []

        j = 0
        while value_2d[0][j][2] >= salary_cap/9:
            j += 1

        lineup.append((value_2d[0][j][0], value_2d[0][j][1], value_2d[0][j][2]))
        update.append(value_2d[0][j][2]) # salary

        for i in range(1, 9):
            k = 0
            while (lineup[i-1] == value_2d[i][k][0] or (value_2d[i][k][2] + update[i-1]) >= (salary_cap/9)*(i+1)):
                k += 1
            lineup.append((value_2d[i][k][0], value_2d[i][k][1], value_2d[i][k][2]))
            update.append(value_2d[i][k][2])

        return lineup

    def pack5(items,sizeLimit):
        P = {}
        for nItems in range(len(items)+1):
            for lim in range(sizeLimit+1):
                if nItems == 0:
                    P[nItems,lim] = 0
                elif itemSize(items[nItems-1]) > lim:
                    P[nItems,lim] = P[nItems-1,lim]
                else:
                    P[nItems,lim] = max(P[nItems-1,lim],
                        P[nItems-1,lim-itemSize(items[nItems-1])] +
                        itemValue(items[nItems-1]))
=======
#         for pf in value_2d[7]:
#             salary_2d[7].append(pf[2])
#             salary_2d[8].append(pf[2])
# """

#         update = []
#         lineup = []

#         j = 0
#         while value_2d[0][j][2] >= salary_cap/9:
#             j += 1

#         lineup.append((value_2d[0][j][0], value_2d[0][j][1], value_2d[0][j][2]))
#         update.append(value_2d[0][j][2]) # salary

#         for i in range(1, 9):
#             k = 0
#             while (lineup[i-1] == value_2d[i][k][0] or (value_2d[i][k][2] + update[i-1]) >= (salary_cap/9)*(i+1)):
#                 k += 1
#             lineup.append((value_2d[i][k][0], value_2d[i][k][1], value_2d[i][k][2]))
#             update.append(value_2d[i][k][2])

#         return lineup

#     def pack5(items,sizeLimit):
#         P = {}
#         for nItems in range(len(items)+1):
#             for lim in range(sizeLimit+1):
#                 if nItems == 0:
#                     P[nItems,lim] = 0
#                 elif itemSize(items[nItems-1]) > lim:
#                     P[nItems,lim] = P[nItems-1,lim]
#                 else:
#                     P[nItems,lim] = max(P[nItems-1,lim],
#                         P[nItems-1,lim-itemSize(items[nItems-1])] +
#                         itemValue(items[nItems-1]))


#         L = []
#         nItems = len(items)
#         lim = sizeLimit
#         while nItems > 0:
#             if P[nItems,lim] == P[nItems-1,lim]:
#                 nItems -= 1
#             else:
#                 nItems -= 1
#                 L.append(itemName(items[nItems]))
#                 lim -= itemSize(items[nItems])

#         L.reverse()
#         return L

#    def knapsack(items, maxweight):
#     """
#     Solve the knapsack problem by finding the most valuable
#     subsequence of `items` subject that weighs no more than
#     `maxweight`.

#     `items` is a sequence of pairs `(value, weight)`, where `value` is
#     a number and `weight` is a non-negative integer.

#     `maxweight` is a non-negative integer.

#     Return a pair whose first element is the sum of values in the most
#     valuable subsequence, and whose second element is the subsequence.

#     >>> items = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
#     >>> knapsack(items, 15)
#     (11, [(2, 1), (6, 4), (1, 1), (2, 2)])
#     """

#     # Return the value of the most valuable subsequence of the first i
#     # elements in items whose weights sum to no more than j.
#     @memoized
#     def bestvalue(i, j):
#         if i == 0: return 0
#         value, weight = items[i - 1]
#         if weight > j:
#             return bestvalue(i - 1, j)
#         else:
#             return max(bestvalue(i - 1, j),
#                        bestvalue(i - 1, j - weight) + value)

#     j = maxweight
#     result = []
#     for i in xrange(len(items), 0, -1):
#         if bestvalue(i, j) != bestvalue(i - 1, j):
#             result.append(items[i - 1])
#             j -= items[i - 1][1]
#     result.reverse()
#     return bestvalue(len(items), maxweight), result
