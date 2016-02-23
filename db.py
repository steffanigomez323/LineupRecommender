from app import app
from scrapers import SwishScraper


class Updater(object):
    def update_base_db(self):
        ss = SwishScraper()
        data = ss.get_players_request()
        players = ss.clean_players_data(data)

        for player in players:
            identifier = player['player_id']
            name = player['player_name']
            team = player['team_abbr']
            position = player['primary_pos_abbr']

            app.database.hmset(identifier, {'name': name,
                                            'team': team,
                                            'position': position})
