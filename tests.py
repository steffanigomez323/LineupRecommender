"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Unit Testing
"""

from app import app
from app import redis_db
from app import swish_scraper
import unittest


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
        redis_db.set('foo', 'bar')
        self.assertEqual(redis_db.get('foo'), 'bar')
        redis_db.delete('foo')


class SwishTestCase(unittest.TestCase):
    # test whether we're able to get data from swish analytics
    def test_data_consistency(self):
        data = swish_scraper.get_projections()
        projections = swish_scraper.clean_projections(
            data, ['player_id'])

        self.assertTrue(len(projections) > 0)


if __name__ == '__main__':
    unittest.main()
