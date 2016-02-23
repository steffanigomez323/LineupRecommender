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

    def clean_players_data(self, data, fields=['player_name', 'team_abbr', 'primary_pos_abbr']):
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
        projections_data = re.search('self.model.masterPlayerArray = (....*?);', data).group(1)
        projections_json = json.loads(projections_data)
        return projections_json

    def clean_projections_data(self, data, fields=['player_name', 'team_abr', 'opp_abr',
                'proj_fantasy_pts_fd', 'fd_salary', 'fd_pos', 
                'injury_status', 'starter']):
        for entry in data:
            for key in deepcopy(entry):
                if key not in fields:
                    del(entry[key])
        return data

# Example data
# {"event_id":"1571679","team_short":"Thunder","team_abr":"OKC",
# "opp_abr":"CLE","player_name":"Russell Westbrook","team":"25",
# "player_id":"329830","event_status_id":"4","risk":"1.1",
# "proj_fantasy_pts_fd":"47.83","proj_fantasy_pts_dk":"52.37",
# "proj_fantasy_pts_ya":"48.39","fd_risk_1":"39.91768620605327",
# "fd_risk_2":"46.1821406106529","fd_risk_3":"52.15522504294535",
# "fd_risk_4":"56.86570626190804","dk_risk_1":"43.706653284779634",
# "dk_risk_2":"50.56572661049326","dk_risk_3":"57.10577326989437",
# "dk_risk_4":"62.2633710419428","ya_risk_1":"40.38504778404595",
# "ya_risk_2":"46.72284725380502","ya_risk_3":"52.76586535287739",
# "ya_risk_4":"57.5314975123088","fd_salary":"10900","dk_salary":
# "11000","ya_salary":"60","fd_pos":"PG","dk_pos":"PG",
# "ya_pos":"PG","value":null,"locked":"0","game":null,
# "news_date":null,"news_category":null,"news_title":null,
# "news_advice":null,"news_link":null,"injury_status":"","starter":"*"}

# * means that the player is a starter | empty means that they are not
# empty injury status means that the player is not injured
