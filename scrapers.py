"""
CS1951A Final Project
Brown University
Spring 2015

Vann, Steffani, JJ, Chaitu

Scrapers
"""

import urllib
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
