from app import app
import unittest

class RedisTest(unittest.TestCase):
    # test whether a connection to redis can be established
    def test_redis_connection(self):
        app.database.set('foo', 'bar')
        self.assertEqual(app.database.get('foo'), 'bar')
        app.database.delete('foo')

if __name__ == '__main__':
    unittest.main()
