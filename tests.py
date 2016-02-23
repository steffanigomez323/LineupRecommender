from app import app
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
        app.database.set('foo', 'bar')
        self.assertEqual(app.database.get('foo'), 'bar')
        app.database.delete('foo')

# class SwishTestCase(unittest.TestCase):
    # test whether swish analytics nba optimus page can be accessed


if __name__ == '__main__':
    unittest.main()
