from openopt import *
from sys import argv
import csv
from collections import namedtuple


class LineupOptimizer(object):

    def __init__(self, player_sack, budget=60000, solver="glpk"):
        self.player_sack = player_sack
        self.budget = budget
        self.solver = solver

    def optimize(self):
        all_ids = range(self.player_sack[-1]['player_id'] + 1)

        constraints = lambda values: (
                # salary cap constraint
                values['cost'] <= self.budget,

                # position constraints
                values['small_forward'] == 2,
                values['power_forward'] == 2,
                values['point_guard'] == 2,
                values['shooting_guard'] == 2,
                values['center'] == 1
            ) + tuple([values['id' + str(i)] <= 1 for i in all_ids])

        objective = 'score'

        ksp = KSP(objective, self.player_sack, constraints = constraints)
        r = ksp.solve(self.solver, iprint = 1, nProc = 2)

        return r.xf


def load_players(file):
    player_sack = list()
    players = dict()
    num_ids = 0
    ids = set([])
    check_position = lambda x, y: 1 if x == y else 0
    with open(file) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            num_ids += 1
            position = row[1]
            name = row[2] + " " + row[3]
            cost = row[6]
            score = row[4]
            players[name] = {
                "position": position,
                "score": score,
                "cost": cost
            }
            player_sack.append({"player_id": num_ids,
                                "name": name,
                                "small_forward": check_position("SF", position),
                                "power_forward": check_position("PF", position),
                                "shooting_guard": check_position("SG", position),
                                "point_guard": check_position("PG", position),
                                "center": check_position("C", position),
                                "cost": int(cost),
                                "score": float(score)})
    all_ids = range(num_ids + 1)

    for player in player_sack:
        for i in all_ids:
            player['id' + str(i)] = float(player['player_id'] == i)

    return players, player_sack

def write_to_csv(players):
    player_list = list()
    for player_name in players.iterkeys():
        position = players[player_name]['position']
        salary = players[player_name]['cost']
        points = players[player_name]['score']
        player_list.append([position, player_name, salary, points])
    with open('output_csv.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Position', 'Name', 'Salary', 'Points'])
        writer.writerows(player_list)

if __name__ == '__main__':
    csv_file = argv[1]

    players, player_sack = load_players(csv_file)

    write_to_csv(players)

    lo = LineupOptimizer(player_sack)
    lineup = lo.optimize()

    sum_score = 0
    for player in lineup:
        sum_score += float(players[player]['score'])
        print player, players[player]

    print sum_score
