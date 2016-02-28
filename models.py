"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Models
"""

from app import app


class Player(db.postgres_db.Model):

    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    team = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    projected_points = db.Column(db.String) # Change later
    salary = db.Column(db.Integer)
    injury_status = db.Column(db.String)

    def __init__(self, id, name, team, position):
        self.id = id
        self.name = name
        self.team = team
        self.position = position

    def __repr__(self):
        return '<title {}'.format(self.title)

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

    def __str__(self):
        return "\n" + "########## Player ##########" + "\n" \
                + "Name: " + self.name + "\n" + "Team: " + self.team + "\n" \
                + "Position: " + self.position + "\n" \
                + "Projection: " + self.projected_points + "\n" \
                + "Salary: " + self.salary + "\n" \
                + "Injured: " + str(self.injury_status) + "\n" \
                + "############################" + "\n"

    def __eq__(self, other):
        return self.player_id == other.player_id
