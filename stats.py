import requests
import json

class NBA_API(object):
	prefix_url = 'http://stats.nba.com/stats/'

	def get_request(self, path, params={}):
		url = self.prefix_url + path
		r = requests.get(url, params=params)
		print r
		return r.json()

	def get_gamelogs(self):
		path = 'leaguegamelog?Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2015-16&SeasonType=Regular+Season&Sorter=PTS'
		return self.get_request(path)

def main():
	nba = NBA_API()
	gamelogs = nba.get_gamelogs()
	'''
	with open('gamelogs.json', 'w') as f:
		json.dump(gamelogs, f)
	'''

	headers_array = gamelogs['resultSets'][0]['headers']
	id_index = headers_array.index('PLAYER_ID')
	name_index = headers_array.index('PLAYER_NAME')
	team_index = headers_array.index('TEAM_NAME')
	game_date_index = headers_array.index('GAME_DATE')
	field_goal_index = headers_array.index('FGM')
	field_goal_3pt_index = headers_array.index('FG3M')
	free_throw_index = headers_array.index('FTM')
	rebound_index = headers_array.index('REB')
	assist_index = headers_array.index('AST')
	steal_index = headers_array.index('STL')
	block_index = headers_array.index('BLK')
	turnover_index = headers_array.index('TOV')
	points_index = headers_array.index('PTS')

	row_array = gamelogs['resultSets'][0]['rowSet']
	players = {}
	for row in row_array:
		player_id = row[id_index]
		if player_id not in players:
			players[player_id] = {'PLAYER_NAME':row[name_index], 'TEAM_NAME':row[team_index], 'GAMES':[]}
		
		game = {
			'DATE':row[game_date_index],
			'3PT_FG':row[field_goal_3pt_index],
			'2PT_FG':row[field_goal_index]-row[field_goal_3pt_index],
			'FT':row[free_throw_index],
			'REB':row[rebound_index],
			'AST':row[assist_index],
			'STL':row[steal_index],
			'BLK':row[block_index],
			'TOV':row[turnover_index],
			'PTS':row[points_index]
		}
		players[player_id]['GAMES'].append(game)

	with open('players.json', 'w') as f:
		json.dump(players, f)

if __name__ == '__main__':
	main()