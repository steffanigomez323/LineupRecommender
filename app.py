"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Main
"""

from flask import Flask, render_template
from redis import Redis
from data_collector import Stattleship
from data_collector import NumberFireScraper
from data_collector import NBAScraper
#from updater import DailyUpdater
from scorer import FanDuelScorer
from namespace import Namespace
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

# stattleship
nba_stattleship = Stattleship()

# nba
nba_scraper = NBAScraper()

# numberfire
nf_scraper = NumberFireScraper()

# daily updater
#daily_updater = DailyUpdater()

# scorers
fanduel_scorer = FanDuelScorer()

# namespace
namespace = Namespace


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/midterm_report')
def midterm_report():
    return render_template('midterm_report.html')


@app.route('/blog_post_1')
def blog_post_1():
    return render_template('blog_post_1.html')

@app.route('/blog_post_2')
def blog_post_2():
    return render_template('blog_post_2.html')

@app.route('/blog_post_3')
def blog_post_3():
	return render_template('blog_post_3.html')

if __name__ == "__main__":
    app.run(debug=True)
