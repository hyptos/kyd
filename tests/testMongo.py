import ConfigParser
import unittest
from pymongo import MongoClient


class testMongo(unittest.TestCase):

    #test if connexion to mongo is up
    def test_connexion(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))

        PORT = int(config.get('mongo','MONGODB_PORT',0))
        HOST = config.get('mongo','MONGODB_HOST',0)
        self.client = MongoClient(HOST,PORT)
        self.db =  self.client.kydDb
        self.collection = self.db.kyd
        self.assertIsNotNone(self.client)


if __name__ == '__main__':
    unittest.main()
