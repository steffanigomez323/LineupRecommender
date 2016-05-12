"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Update Module
"""

# from app import redis_db
# from app import namespace
from projector import DailyProjector
from db_helper import CSVHelper
from optimizer import LineupOptimizer
import json


class DailyUpdater(object):
    def get_todays_optimal_lineup(self):
        
        print "Step 0: Getting data and creating CSVs."
        # let's first get all the data we need and store it in csvs
        ch = CSVHelper()
        ch.create_csvs()
        print "---> Data successfully stored!"

        print "Step 1: Preparing data from CSVs :)"
        # let's prepare out data for projections
        dp = DailyProjector()
        dp.prepare_data_for_projections("data/numberfire_data_sample.txt")
        print "------> Data is prepared!"

        print "Step 2: Time to make some projections :)"
        # let's get the projections based on the prepared data
        projections = dp.project_fd_score()
        print projections
        print "------> Projections are ready!"

        print "Step 3: Let's get that golden lineup!!!!"
        # let's get the optimal lineup based on the projections
        lo = LineupOptimizer(projections)
        with open('static/data/optimal_lineup.json', 'wb') as ol:
            json.dump(lo.optimize(), ol)
        print "------> Your lineup has been stored in static/data/optimal_lineup.json. \
            Let's make some cash money ;)"
        print "------> This lineup can also be viewed at \
            http://lineup-recommender.herokuapp.com/. Enjoy!"


if __name__ == '__main__':
    du = DailyUpdater()
    du.get_todays_optimal_lineup()