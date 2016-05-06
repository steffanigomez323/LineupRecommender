"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Data Collector
"""

import urllib
import re
from requestor import CustomRequest
from bs4 import BeautifulSoup
from copy import deepcopy
from collections import defaultdict
from datetime import datetime


class NBAStattleShip(object):
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


class NumberFireScraper(object):

    def get_player_name_slug_map(self):
        url = 'https://www.numberfire.com/nba/players/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        data = soup.find_all('p', attrs={'class': 'sb'})

        name_to_slug = {}

        for d in data:
            name_position_team = d.text
            name_match = re.search('(^[^,]+)(PG|GF|PF|FC|SG|SF)', name_position_team) # match 2 first
            
            if name_match == None:
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

        players = list()

        for i in range(len(data)):
            if i < 2:
                continue

            player_raw = data[i].find('td', attrs={'class': 'player'})
            playing_at_home_raw = data[i].find('td', attrs={'class': 'sep'})
            salary_raw = data[i].find('td', attrs={'class': 'col-salary'})

            # working with playing_at_home
            if '@' in playing_at_home_raw.text:
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

            position_match = re.search('\((.*),', player_raw.text)
            if position_match:
                position = position_match.group(1)

            status = player_raw.find('span', attrs={'class': 'injury-tag-OUT'})
            if status:
                out = (status.text == "OUT")
            else:
                out = False

            # get who they are playing against as well
            if salary_match and position_match and not out:
                players.append((player_id, position, playing_at_home, salary))

        return players


class NBAScraper(object):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

    def __init__(self):
        self.nba_request = CustomRequest("http://stats.nba.com/stats/",
                                         self.headers)

    def get_player_data(self):
        modifier = 'commonallplayers'
        params = {'IsOnlyCurrentSeason': '1',
                  'LeagueID': '00',
                  'Season': '2015-16'}
        result = self.nba_request.get_request(modifier, params)

        return result.json()

    def get_player_name_id_map(self, data):
        headers = data['resultSets'][0]['headers']
        values = data['resultSets'][0]['rowSet']

        player_id_index = headers.index('PERSON_ID')
        name_index = headers.index('DISPLAY_FIRST_LAST')

        name_to_id = {}

        for value in values:
            player_id = value[player_id_index]
            name = value[name_index]
            name_to_id[name] = str(player_id)

        return name_to_id

    def get_player_stats(self, season):
        modifier = 'leaguegamelog'
        params = {'Direction': 'DESC',
                  'LeagueID': '00',
                  'PlayerOrTeam': 'P',
                  'Season': season,
                  'SeasonType': 'Regular Season',
                  'Sorter': 'PTS'}

        result = self.nba_request.get_request(modifier, params)

        return result.json()

    def clean_player_stats(self, data):
        headers_array = data['resultSets'][0]['headers']
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

        row_array = data['resultSets'][0]['rowSet']
        players = {}
        for row in row_array:
            player_id = row[id_index]
            if player_id not in players:
                players[player_id] = {'PLAYER_NAME': row[name_index],
                                      'TEAM_NAME': row[team_index],
                                      'GAMES': []}

            game = {
                'DATE': row[game_date_index],
                #'3PT_FG': row[field_goal_3pt_index],
                #'2PT_FG': row[field_goal_index]-row[field_goal_3pt_index],
                #pst'FT': row[free_throw_index],
                'REB': row[rebound_index],
                'AST': row[assist_index],
                'STL': row[steal_index],
                'BLK': row[block_index],
                'TOV': row[turnover_index],
                'PTS': row[points_index]
            }

            players[player_id]['GAMES'].append(game)

        return players

    def clean_player_stats2(self, data):
        headers_array = data['resultSets'][0]['headers']
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

        row_array = data['resultSets'][0]['rowSet']
        players = {}
        for row in row_array:
            player_id = row[id_index]
            if player_id not in players:
                players[player_id] = {'player_name': row[name_index].lower(),
                                      'team_name': row[team_index],
                                      'games': []}
            d = row[game_date_index].split("-")
            gtime = datetime(int(d[0]), int(d[1]), int(d[2]))
            matchup = row[matchup_index].lower().split(" ")
            at_home = True
            if matchup[1] == "@":
                at_home = False
            game = {
                'game_id': row[game_id_index],
                'game_time': gtime.isoformat(),
                'played_at_home': at_home,
                'played_against': 'nba-' + matchup[len(matchup) - 1],
                'plus_minus': row[plus_minus_index],
                'time_played_total': int(row[time_played_index]) * 60,
                'rebounds_total': row[rebound_index],
                'assists': row[assist_index],
                'steals': row[steal_index],
                'blocks': row[block_index],
                'turnovers': row[turnover_index],
                'points': row[points_index]
            }

            players[player_id]['games'].append(game)


        game_time = []
        played_at_home = []
        played_against = []
        plus_minus = []
        time_played_total = []
        rebounds_total = []
        assists = []
        steals = []
        blocks = []
        turnovers = []
        points = []

        for p in players:
            for i in range (0, len(players[p]['games'])):
                game_time.append(players[p]['games'][i]['game_time'])
                played_against.append(players[p]['games'][i]['played_against'])
                played_at_home.append(players[p]['games'][i]['played_at_home'])
                plus_minus.append(players[p]['games'][i]['plus_minus'])
                time_played_total.append(players[p]['games'][i]['time_played_total'])
                rebounds_total.append(players[p]['games'][i]['rebounds_total'])
                assists.append(players[p]['games'][i]['assists'])
                steals.append(players[p]['games'][i]['steals'])
                blocks.append(players[p]['games'][i]['blocks'])
                turnovers.append(players[p]['games'][i]['turnovers'])
                points.append(players[p]['games'][i]['points'])

            players[p]['games'] = {
                'game_time': game_time,
                'played_at_home': played_at_home,
                'played_against': played_against,
                'plus_minus': plus_minus,
                'time_played_total': time_played_total,
                'rebounds_total': rebounds_total,
                'assists': assists,
                'steals': steals,
                'blocks': blocks,
                'turnovers': turnovers,
                'points': points
            }
            game_time = []
            played_at_home = []
            played_against = []
            plus_minus = []
            time_played_total = []
            rebounds_total = []
            assists = []
            steals = []
            blocks = []
            turnovers = []
            points = []

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
