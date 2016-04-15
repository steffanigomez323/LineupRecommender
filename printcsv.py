from simple_recommender import SimpleRecommender
from updater import DailyUpdate
from redis import Redis
from scrapers import SwishScraper
from scrapers import NBAScraper
from id_manager import IDManager
import csv


def writeCSV():
	c = csv.writer(open("lineup.csv", "wb"))
	c.writerow(["Name","Team","Position","Projection","Salary","Injury Status"])
	u = DailyUpdate()
	players = u.get_projections()
	s = SimpleRecommender(players)
	lineup = s.get_simple_lineup()
	for player in lineup:
		c.writerow([player.name, player.team, player.position, player.projected_points, player.salary, player.injury_status])

if __name__ == "__main__":
    writeCSV()