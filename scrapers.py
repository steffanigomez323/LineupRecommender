"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Scrapers
"""

import urllib
import requests
import json
import re
from bs4 import BeautifulSoup
from copy import deepcopy


class SwishScraper(object):

    def get_players_request(self):
        url = 'https://www.swishanalytics.com/nba/players/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        data = soup.find_all('script')[4].string
        players_data = re.search('this.all_players = (.*?);', data).group(1)
        players_json = json.loads(players_data)
        return players_json

    def clean_players_data(self, data, fields=['player_id',
                                               'player_name',
                                               'team_abbr',
                                               'primary_pos_abbr']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])
        return data

    def get_projections_request(self):
        url = 'https://www.swishanalytics.com/optimus/nba/optimus-x/'
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        data = soup.find_all('script')[9].string
        projections_data = re.search(
            'self.model.masterPlayerArray = (....*?);', data).group(1)
        projections_json = json.loads(projections_data)
        return projections_json

    def clean_projections_data(self, data, fields=['player_id',
                                                   'player_name',
                                                   'proj_fantasy_pts_fd',
                                                   'fd_salary',
                                                   'fd_pos',
                                                   'team_abr',
                                                   'injury_status']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])
        return data


class NBAScraper(object):

    def get_player_stats_request(self):
        url = ('http://stats.nba.com/stats/leaguegamelog?Direction=DESC'
               '&LeagueID=00&PlayerOrTeam=P&Season=2015-16&SeasonType=R'
               'egular+Season&Sorter=PTS')
        r = requests.get(url)
        return r.json()

    def clean_player_stats_data(self, data):
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
