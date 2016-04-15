"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Scrapers
"""

import urllib
from custom_request import CustomRequest
import json
import re
from bs4 import BeautifulSoup
from copy import deepcopy


class SwishScraper(object):

    def get_players(self):
        url = 'https://www.swishanalytics.com/nba/players/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        data = soup.find_all('script')[4].string
        players_data = re.search('this.all_players = (.*?);', data).group(1)
        players_json = json.loads(players_data)
        return players_json

    def clean_players(self, data, fields=['player_id',
                                          'player_name',
                                          'team_abbr',
                                          'primary_pos_abbr']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])

        swish_dict = {}
        for entry in data:
            swish_dict[entry['player_name']] = (entry['player_id'],
                                                entry['team_abbr'],
                                                entry['primary_pos_abbr'])

        return swish_dict

    def get_projections(self):
        url = 'https://www.swishanalytics.com/optimus/nba/optimus-x/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        data = soup.find_all('script')[9].string
        projections_data = re.search(
            'self.model.masterPlayerArray = (....*?);', data).group(1)
        projections_json = json.loads(projections_data)
        return projections_json

    def clean_projections(self, data, fields=['player_id',
                                              'proj_fantasy_pts_fd',
                                              'fd_salary',
                                              'injury_status']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])
        return data


class NBAStattleShip(object):
    headers = {'content-type': 'application/json',
               'authorization': 'Token token=067adb3fdbd52c6a8c12331152bf262f',
               'accept': 'application/vnd.stattleship.com; version=1'}

    def __init__(self):
        self.nba_request = \
            CustomRequest("https://www.stattleship.com/basketball/nba/",
                          self.headers)

    def get_players(self):
        modifier = 'players'

        result = self.nba_request.get_request(modifier)

        return result.json()

    def get_game_logs(self):
        


class NBAScraper(object):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
               (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

    def __init__(self):
        self.nba_request = CustomRequest("http://stats.nba.com/stats/",
                                         self.headers)

    def get_players(self):
        modifier = 'commonallplayers'
        params = {'IsOnlyCurrentSeason': '1',
                  'LeagueID': '00',
                  'Season': '2015-16'}
        result = self.nba_request.get_request(modifier, params)
        return result.json()

    def clean_players(self, data):
        headers = data['resultSets'][0]['headers']
        values = data['resultSets'][0]['rowSet']

        player_id_index = headers.index('PERSON_ID')
        name_index = headers.index('DISPLAY_FIRST_LAST')
        team_id_index = headers.index('TEAM_ID')
        team_abbr_index = headers.index('TEAM_ABBREVIATION')

        nba_dict = {}

        for value in values:
            name = value[name_index]
            match = re.search('.\..\.', name)
            if match:
                name = name.replace(".", "")
            name = name.lower()
            nba_dict[name] = (str(value[player_id_index]),
                              value[team_id_index],
                              value[team_abbr_index],
                              value[name_index])

        return nba_dict

    def get_player_stats(self, season='2015-16'):
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
                '3PT_FG': row[field_goal_3pt_index],
                '2PT_FG': row[field_goal_index]-row[field_goal_3pt_index],
                'FT': row[free_throw_index],
                'REB': row[rebound_index],
                'AST': row[assist_index],
                'STL': row[steal_index],
                'BLK': row[block_index],
                'TOV': row[turnover_index],
                'PTS': row[points_index]
            }

            players[player_id]['GAMES'].append(game)

        return players
