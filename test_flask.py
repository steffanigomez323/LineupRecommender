from app import app
import unittest

class FlaskTest(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()