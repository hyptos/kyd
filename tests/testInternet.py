import unittest
import requests


class testInternet(unittest.TestCase):

    #test if an internet connexion is up
    def test_InternetConnexion(self):
        r = requests.get('http://google.com')
        self.assertIs(r.status_code,200)

if __name__ == '__main__':
    unittest.main()
