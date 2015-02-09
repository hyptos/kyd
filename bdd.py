import ConfigParser
import datetime
from pymongo import MongoClient

class ClientMongo():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))

        PORT = int(config.get('mongo','MONGODB_PORT',0))
        HOST = config.get('mongo','MONGODB_HOST',0)
        self.client = MongoClient(HOST,PORT)
        self.db =  self.client.kydDb
        self.collection = self.db.kyd


# donnees de tests
test = {
    'ip': '192.168.1.1',
    'latitude': 2.22,
    'longitude': 2.22,
    'city': 'Villeurbanne',
    'country': 'France',
    'drive': 'googledrive',
    'interface': 'sdk',
    'start_date': datetime.datetime.now(),
    'size': 80000,
    'transfert': 'download',
    'time':2.22
}

if __name__ == "__main__":
    print 'start'
    c = ClientMongo()
    # c.collection.insert(test)