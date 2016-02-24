"""
CS1951A Final Project
Brown University
Spring 2015

Vann, Steffani, JJ, Chaitu

Unit Testing
"""

from app import app
import unittest
from scrapers import SwishScraper


class FlaskTestCase(unittest.TestCase):
    # test whether index loads
    def test_index_response(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # test whether writeup loads
    def test_writeup_response(self):
        tester = app.test_client(self)
        response = tester.get('/writeup', content_type='html/text')
        self.assertEqual(response.status_code, 200)


class RedisTestCase(unittest.TestCase):
    # test whether a connection to redis can be established
    def test_redis_connection(self):
        app.database.set('foo', 'bar')
        self.assertEqual(app.database.get('foo'), 'bar')
        app.database.delete('foo')


class SwishTestCase(unittest.TestCase):
    # test whether the data stored in our database
    # is consistent with swish projections
    def test_data_consistency(self):
        ss = SwishScraper()
        data = ss.get_projections_request()
        projections = ss.clean_projections_data(
            data, ['player_id', 'player_name', 'fd_pos', 'team_abr'])

        for projection in projections:
            player_id = projection['player_id']
            self.assertTrue(app.database.exists(player_id))


if __name__ == '__main__':
    unittest.main()
