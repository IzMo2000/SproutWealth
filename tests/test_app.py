import unittest, sys, os

sys.path.append('../SproutWealth') # imports python file from parent directory
from app import app

class AppTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_result_page(self):
        response = self.app.get('/result', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # ... test routes

    # 

if __name__ == "__main__":
    unittest.main()
