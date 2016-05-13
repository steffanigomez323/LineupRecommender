"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Data Collector
"""

import urllib
import re
from namespace import Namespace
from requestor import CustomRequest
from bs4 import BeautifulSoup
from copy import deepcopy
from collections import defaultdict
from datetime import datetime
import numpy as np

'''
We collect the following information from Stattleship:
- player name slug
- weight
- height
- whether or not a player is active
- years of experience
'''
class Stattleship(object):
    headers = {'content-type': 'application/json',
               'authorization': 'Token token=067adb3fdbd52c6a8c12331152bf262f',
               'accept': 'application/vnd.stattleship.com; version=1'}

    def __init__(self):
        self.nba_request = \
            CustomRequest("https://www.stattleship.com/basketball/nba/",
                          self.headers)

    def get_player_data(self):
        modifier = 'players'

        response = self.nba_request.get_request(modifier)
        data = response.json()['players']

        while 'next' in response.links:
            modifier = re.match(self.nba_request.base_url + '(.*)',
                                response.links['next']['url']).group(1)
            response = self.nba_request.get_request(modifier)
            data.extend(response.json()['players'])

        return data

    def get_player_fields(self, data, fields=['slug',
                                              'active',
                                              'name',
                                              'weight',
                                              'height',
                                              'years_of_experience']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])

        return data

    def get_player_name_slug_map(self, data):
        name_id = {}
        for entry in data:
            name = entry['name']
            slug = entry['slug']
            name_id[name] = slug

        return name_id

    def get_team_data(self):
        modifier = 'teams'

        response = self.nba_request.get_request(modifier)
        data = response.json()['teams']

        while 'next' in response.links:
            modifier = re.match(self.nba_request.base_url + '(.*)',
                                response.links['next']['url']).group(1)
            response = self.nba_request.get_request(modifier)
            data.extend(response.json()['teams'])

        return data

    def get_team_fields(self, data, fields=['id',
                                            'slug']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])

        return data

    def get_team_id_to_slug(self):
        team_data = self.get_team_data()
        relevant_data = self.get_team_fields(team_data)

        id_to_slug = {}

        for field in relevant_data:
            id_to_slug[field['id']] = field['slug']

        return id_to_slug

    def get_player_stats_data(self, player_id, fields={
                              'basketball_defensive_stat':
                              ['blocks', 'steals'],
                              'basketball_offensive_stat':
                              ['points', 'turnovers', 'assists'],
                              'basketball_player_stat':
                              ['plus_minus', 'time_played_total'],
                              'basketball_rebounding_stat':
                              ['rebounds_total']},
                              seasons=['nba-2015-2016',
                                       'nba-2014-2015',
                                       'nba-2013-2014',
                                       'nba-2012-2013',
                                       'nba-2011-2012']):
        # STATS #
        # defensive - basketball_defensive_stat #
        # - blocks
        # - steals
        # offensive - basketball_offensive_stat #
        # - assists
        # - field_goals_attempted
        # - field_goals_made
        # - free_throws_attempted
        # - free_throws_made
        # - points
        # - three_pointers_attempted
        # - three_pointers_made
        # - turnovers
        # player - basketball_player_stat #
        # - disqualifications
        # - personal_fouls
        # - plus_minus
        # - points
        # - technical_fouls
        # - time_played_total
        # rebounding - basketball_rebounding_stat #
        # - rebounds_defensive
        # - rebounds_offensive
        # - rebounds_total
        data = defaultdict(list)

        for stat_type, stat_list in fields.iteritems():
            for stat_name in stat_list:
                modifier = 'stats?type=' + stat_type + \
                           '&stat=' + stat_name + \
                           '&player_id=' + player_id + \
                           '&interval_type=regularseason'

                response = self.nba_request.get_request(modifier)
                if len(response.json()['stats']) != 0:

                    for game in response.json()['stats']:
                        data[stat_name].append(game['stat'])

                    while 'next' in response.links:
                        modifier = re.match(self.nba_request.base_url + '(.*)',
                                            response.links['next']['url']).group(1)
                        response = self.nba_request.get_request(modifier)
                        for game in response.json()['stats']:
                            data[stat_name].append(game['stat'])

        return data

    def get_game_log_data(self, player_id):
        modifier = 'game_logs?player_id=' + \
                   player_id + \
                   '&interval_type=regularseason'

        response = self.nba_request.get_request(modifier)

        if len(response.json()['game_logs']) != 0:

            data = {"game_logs": response.json()['game_logs'],
                    "games": response.json()['games']}

            while 'next' in response.links:
                modifier = re.match(self.nba_request.base_url + '(.*)',
                                    response.links['next']['url']).group(1)
                response = self.nba_request.get_request(modifier)
                data['game_logs'].extend(response.json()['game_logs'])
                data['games'].extend(response.json()['games'])

            return data

        return None

    def prepare_data_for_projections(self, player_id):
        id_to_slug = self.get_team_id_to_slug()

        stats = self.get_player_stats_data(player_id)
        game_logs = self.get_game_log_data(player_id)

        if game_logs != None:

            stats['game_time'] = list()
            stats['played_at_home'] = list()
            stats['played_against'] = list()

            for i in range(len(stats['plus_minus'])):
                game_time = game_logs['games'][i]['started_at']
                stats['game_time'].append(game_time)

                opponent = id_to_slug[game_logs['game_logs'][i]['opponent_id']]
                stats['played_against'].append(opponent)

                if game_logs['game_logs'][i]['team_id'] == \
                        game_logs['games'][i]['home_team_id']:
                    stats['played_at_home'].append(True)
                else:
                    stats['played_at_home'].append(False)

            print stats
            print ""

            data = self.clean_data_for_projections(stats)

            return data

        return None

    def clean_data_for_projections(self, data):
        time_played = deepcopy(data['time_played_total'])

        deleted_count = 0

        for i in range(len(time_played)):
            if time_played[i] is None:
                for stat in data.iterkeys():
                    del data[stat][i - deleted_count]
                deleted_count += 1

        for stat_name, per_game_list in data.iteritems():
            for i, stat in enumerate(per_game_list):
                if stat is None:
                    per_game_list[i] = 0

        return data

'''
We collect the following information about a player from NumberFire:
- salary
- player position
- opponent
- whether the player played at home or away
'''
class NumberFireScraper(object):

    def get_player_name_slug_map(self):
        url = 'https://www.numberfire.com/nba/players/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        data = soup.find_all('p', attrs={'class': 'sb'})

        name_to_slug = {}

        for d in data:
            name_position_team = d.text
            name_match = re.search('(^[^,]+)(PG|GF|PF|FC|SG|SF)',
                                   name_position_team)

            if not name_match:
                name_match = re.search('(^[^,]+)(G|F|C)', name_position_team)

            name = name_match.group(1)
            link_text = d.a['href']
            link_match = re.search('/nba/players/(.*)', link_text)
            name_to_slug[name] = link_match.group(1)

        return name_to_slug

    def get_todays_player_data(self):
        url = 'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        data = soup.find_all('tr')

        players = dict()

        for i in range(len(data)):
            if i < 2:
                continue

            player_raw = data[i].find('td', attrs={'class': 'player'})
            team_details_raw = data[i].find('td', attrs={'class': 'sep'})
            salary_raw = data[i].find('td', attrs={'class': 'col-salary'})

            # working with team details
            opponent_match = re.search('([A-Z])\w+', team_details_raw.text)
            if opponent_match:
                opponent = Namespace().TEAM_MAP_NF_NBA[opponent_match.group(0)]
            if '@' in team_details_raw.text:
                playing_at_home = False
            else:
                playing_at_home = True

            # working with salary
            salary_match = re.match('\$(.*)', salary_raw.text)
            if salary_match:
                salary = salary_match.group(1)

            # working with player
            link = player_raw.a['href']
            link_match = re.search('/nba/players/(.*)', link)
            player_id = link_match.group(1)

            # working with position
            position_match = re.search('\((.*),', player_raw.text)
            if position_match:
                position = position_match.group(1)

            # working with team
            team_match = re.search(',\s(.*)\)', player_raw.text)
            if team_match:
                team = Namespace().TEAM_MAP_NF_NBA[team_match.group(1)]

            # working with status
            status = player_raw.find('span', attrs={'class': 'injury-tag-OUT'})
            if status:
                out = (status.text == "OUT")
            else:
                out = False

            # get who they are playing against as well
            if salary_match and position_match and not out:
                players[player_id] = {"position": position,
                                      "playing_at_home": playing_at_home,
                                      "salary": salary,
                                      "playing_against": opponent,
                                      "team": team}

        return players

'''
We collect the following information about the players from NBA:
- the game logs of each player: each game log stores the following information:
    - Time the game was held
    - Information on whether the game was played at home or away
    - The opponent team
    - Plus minus
    - How many times the player played in that game
    - Total rebounds score for the team the player is in
    - Total assists score
    - Total steals score
    - Total blocks score
    - Total turnovers score
    - Total points
'''
class NBAScraper(object):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

    def __init__(self):
        self.nba_request = CustomRequest("http://stats.nba.com/stats/",
                                         self.headers)

    def get_player_data(self, seasons=['2012-13',
                                       '2013-14',
                                       '2014-15',
                                       '2015-16']):
        players = []
        for season in seasons:
            modifier = 'commonallplayers'
            params = {'IsOnlyCurrentSeason': '1',
                      'LeagueID': '00',
                      'Season': season}

            result = self.nba_request.get_request(modifier, params)

            players.append(result.json())
        return players

    def get_player_position(self, playerid):

        modifier = 'commonplayerinfo'
        params = {'PlayerID': playerid,
                  'LeagueID': '00'}
        result = self.nba_request.get_request(modifier, params).json()
        headers = result['resultSets'][0]['headers']
        values = result['resultSets'][0]['rowSet']

        position_id_index = headers.index('POSITION')

        position = ""
        for value in values:
            position = value[position_id_index]
            # Some players play multiple positions, but the informatoin is
            # not explicit. Ex: if a player's position is Center-Forward,
            # it means they play both Center and Power Forward positions.
            if position.encode('utf-8') == "Center-Forward":
                pos_arr = ['C', 'PF']
            elif position.encode('utf-8') == "Guard-Forward":
                pos_arr = ['SF', 'PG']
            elif position.encode('utf-8') == "Forward-Center":
                pos_arr = ['SF', 'C']
            elif position.encode('utf-8') == "Guard":
                pos_arr = ['PG', 'SG']
            elif position.encode('utf-8') == "Forward":
                pos_arr = ['PF', 'SF']
            elif position.encode('utf-8') == "Forward-Guard":
                pos_arr = ['PF', 'SG']
            elif position.encode('utf-8') == "Center":
                pos_arr = ['C']
            else:
                pos_arr = ['UN']

        return pos_arr

    def get_player_name_id_map(self, data):
        name_to_id = {}
        for d in data:
            headers = d['resultSets'][0]['headers']
            values = d['resultSets'][0]['rowSet']

            player_id_index = headers.index('PERSON_ID')
            name_index = headers.index('DISPLAY_FIRST_LAST')

            for value in values:
                player_id = value[player_id_index]
                name = value[name_index]
                if name not in name_to_id:
                    name_to_id[name] = str(player_id)

        return name_to_id

    def get_player_stats(self, seasons=['2012-13',
                                        '2013-14',
                                        '2014-15',
                                        '2015-16']):
        j = []
        for s in seasons:
            modifier = 'leaguegamelog'
            params = {'Direction': 'DESC',
                      'LeagueID': '00',
                      'PlayerOrTeam': 'P',
                      'Season': s,
                      'SeasonType': 'Regular Season',
                      'Sorter': 'PTS'}

            result = self.nba_request.get_request(modifier, params)
            j.append(result.json())
        return j


    # returns a dictionary of players and their game logs for the past 4 seasons.
    # sorted from oldest to most recent game

    # 0 = game_id
    # 1 - game_time
    # 2 - played_at_home
    # 3 - played_against
    # 4 - plus_minus
    # 5 - time_played_total
    # 6 - rebounds_total
    # 7 - assists
    # 8 - steals
    # 9 - blocks
    # 10 - turnovers
    # 11 - points


    #def clean_player_stats(self, data):
    def prepare_data_for_projections(self, data):
        players = {}
        for season in data:
            headers_array = season['resultSets'][0]['headers']
            id_index = headers_array.index('PLAYER_ID')
            name_index = headers_array.index('PLAYER_NAME')
            team_index = headers_array.index('TEAM_NAME')
            game_date_index = headers_array.index('GAME_DATE')
            game_id_index = headers_array.index('GAME_ID')
            #field_goal_index = headers_array.index('FGM')
            #field_goal_3pt_index = headers_array.index('FG3M')
            #free_throw_index = headers_array.index('FTM')
            plus_minus_index = headers_array.index('PLUS_MINUS')
            matchup_index = headers_array.index('MATCHUP')
            time_played_index = headers_array.index('MIN')
            rebound_index = headers_array.index('REB')
            assist_index = headers_array.index('AST')
            steal_index = headers_array.index('STL')
            block_index = headers_array.index('BLK')
            turnover_index = headers_array.index('TOV')
            points_index = headers_array.index('PTS')

            row_array = season['resultSets'][0]['rowSet']

            for row in row_array:
                player_id = row[id_index]
                if player_id not in players:
                    players[player_id] = {'player_name': row[name_index].lower(),
                                          'team_name': row[team_index],
                                          'games': [],
                                          'allgames': []}
                d = row[game_date_index].split("-")
                gtime = datetime(int(d[0]), int(d[1]), int(d[2]))
                matchup = row[matchup_index].lower().split(" ")
                at_home = True
                if matchup[1] == "@":
                    at_home = False

                game = {
                    'game_id': int(row[game_id_index]),
                    'game_time': int(gtime.strftime("%s")) * 1000, #gtime.isoformat(),
                    'played_at_home': at_home,
                    'played_against': 'nba-' + matchup[len(matchup) - 1],
                    'plus_minus': int(row[plus_minus_index]),
                    'time_played_total': int(row[time_played_index]),
                    'rebounds_total': int(row[rebound_index]),
                    'assists': int(row[assist_index]),
                    'steals': int(row[steal_index]),
                    'blocks': int(row[block_index]),
                    'turnovers': int(row[turnover_index]),
                    'points': int(row[points_index])
                }

                players[player_id]['games'].append(game)

            for p in players:

                for i in range (0, len(players[p]['games'])):
                    game_list = [
                        players[p]['games'][i]['game_id'],
                        players[p]['games'][i]['game_time'],
                        players[p]['games'][i]['played_against'],
                        players[p]['games'][i]['played_at_home'],
                        players[p]['games'][i]['plus_minus'],
                        players[p]['games'][i]['time_played_total'],
                        players[p]['games'][i]['rebounds_total'],
                        players[p]['games'][i]['assists'],
                        players[p]['games'][i]['steals'],
                        players[p]['games'][i]['blocks'],
                        players[p]['games'][i]['turnovers'],
                        players[p]['games'][i]['points']
                    ]
                    players[p]['allgames'].append(np.array(game_list))

                players[p]['games'] = []

        for p in players:
            players[p]['allgames'] = np.array(players[p]['allgames'])
            ordered = sorted(players[p]['allgames'], key=lambda x: x[0])
            players[p]['allgames'] = ordered

        return players



# class SwishScraper(object):

#     def get_players(self):
#         url = 'https://www.swishanalytics.com/nba/players/'
#         page = urllib.urlopen(url)
#         soup = BeautifulSoup(page, 'lxml')
#         data = soup.find_all('script')[4].string
#         players_data = re.search('this.all_players = (.*?);', data).group(1)
#         players_json = json.loads(players_data)
#         return players_json

#     def clean_players(self, data, fields=['player_id',
#                                           'player_name',
#                                           'team_abbr',
#                                           'primary_pos_abbr']):
#         for entry in data:
#             for key in deepcopy(entry):
#                 if key not in fields:
#                     del(entry[key])

#         swish_dict = {}
#         for entry in data:
#             swish_dict[entry['player_name']] = (entry['player_id'],
#                                                 entry['team_abbr'],
#                                                 entry['primary_pos_abbr'])

#         return swish_dict

#     def get_projections(self):
#         url = 'https://www.swishanalytics.com/optimus/nba/optimus-x/'
#         page = urllib.urlopen(url)
#         soup = BeautifulSoup(page, 'lxml')
#         data = soup.find_all('script')[9].string
#         projections_data = re.search(
#             'self.model.masterPlayerArray = (....*?);', data).group(1)
#         projections_json = json.loads(projections_data)
#         return projections_json

#     def clean_projections(self, data, fields=['player_id',
#                                               'proj_fantasy_pts_fd',
#                                               'fd_salary',
#                                               'injury_status']):
#         for entry in data:
#             for key in deepcopy(entry):
#                 if key not in fields:
#                     del(entry[key])
#         return data
