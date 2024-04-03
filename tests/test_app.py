import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_detect_page_loads(self):
        response = self.app.get('/detect')
        self.assertEqual(response.status_code, 200)

    def test_history_page_loads(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)

    def test_samples_page_loads(self):
        response = self.app.get('/samples')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
