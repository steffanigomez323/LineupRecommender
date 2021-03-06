"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Models
"""

class GameLogs(object):
    def __init__(self, steals, rebounds, points,
                 turnovers, blocks, minutes, plus_minus,
                 hva, opponent, time_stamp):
        '''
        player_gamelogs['steals_pg']
        player_gamelogs['rebounds_pg']
        player_gamelogs['points_pg']
        player_gamelogs['turnovers_pg']
        player_gamelogs['blocks_pg']
        player_gamelogs['minutes_pg']
        player_gamelogs['plus_minus_pg']
        player_gamelogs['hva']
        player_gamelogs['opponent']
        player_gamelogs['time_stamp']
        '''


class Player(object):
    # keep adding init fields as necessary
    def __init__(self, player_id, name, team,
                 position, projected_points,
                 salary, injury_status):
        self.player_id = player_id
        self.name = name
        self.team = team
        self.position = position
        self.projected_points = projected_points
        self.salary = salary
        if injury_status == '':
            self.injury_status = "Not Injured"
        else:
            self.injury_status = injury_status

    def __repr__(self):
        return "\n" + "########## Player ##########" + "\n" \
                + "Name: " + self.name + "\n" + "Team: " + self.team + "\n" \
                + "Position: " + self.position + "\n" \
                + "Projection: " + self.projected_points + "\n" \
                + "Salary: " + self.salary + "\n" \
                + "Injured: " + str(self.injury_status) + "\n" \
                + "############################" + "\n"

    def __eq__(self, other):
        return self.player_id == other.player_id