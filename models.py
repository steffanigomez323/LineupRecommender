class Player(object):
    # Replace once Team class is implemented
    teams = set(['BOS', 'BKN', 'NY', 'PHI', 'TOR', 'CHI', 'CLE', 'DET',
                 'IND', 'MIL', 'ATL', 'CHA', 'MIA', 'ORL', 'WAS', 'GS',
                 'LAC', 'LAL', 'PHO', 'SAC', 'DAL', 'HOU', 'MEM',
                 'NO', 'SA', 'DEN', 'MIN', 'OKC', 'POR', 'UTA'])

    # replace once Position class is implemented
    positions = set(['PG', 'SG', 'SF', 'PF', 'C'])

    # keep adding init fields as necessary
    def __init__(self, player_id, name, team, position):
        self.player_id = player_id
        self.name = name
        if team not in self.teams:
            raise Exception('Invalid team.')
        self.team = team
        if position not in self.positions:
            raise Exception('Invalid position.')
        self.position = position

    def __str__(self):
        return "Name: " + self.name + "\n" + "Team: " + self.team + "\n" \
                + "Position: " + self.position

    def __eq__(self, other):
        return self.player_id == other.player_id

# class Team(object): TODO

# class Positions(object): TODO
