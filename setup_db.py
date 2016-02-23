from app import app
from swish import SwishScraper

ss = SwishScraper()
data = ss.get_players_request()
players = ss.clean_players_data(data)

print players
