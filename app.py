"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Main
"""

from flask import Flask, render_template
from redis import Redis
from scrapers import SwishScraper
from scrapers import NBAScraper
from id_manager import IDManager
from scorer import FanDuelScorer
# from simple_recommender import SimpleRecommender
# import os

app = Flask(__name__)

# config
app.config.from_object('config.DevelopmentConfig')
# USE WHEN DEPLOYING | export APP_SETTINGS = config.ProductionConfig
# app.config.from_object(os.environ['APP_SETTINGS'])

# databases
redis_db = Redis(host=app.config['REDIS_HOST'],
                 port=app.config['REDIS_PORT'],
                 password=app.config['REDIS_PASSWORD'])

# scrapers
swish_scraper = SwishScraper()
nba_scraper = NBAScraper()
id_manager = IDManager()

# scorers
fanduel_scorer = FanDuelScorer()


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/writeup')
def writeup():
    return render_template('writeup.html')

if __name__ == "__main__":
    app.run(debug=True)
