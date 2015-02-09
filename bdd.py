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

    def cleanBdd(self):
        self.collection.remove({})

    def getAllAvgUpload(self):
        pipe = [
            {'$group':{'_id': {'drive' : "$drive", 'transfert':"upload"},'AverageDuration':{'$avg':'$time'}}}
        ]

        return self.collection.aggregate(pipeline=pipe)

    def getAllAvgDownload(self):
        pipe = [
            {'$group':{'_id': {'drive' : "$drive", 'transfert':"download"},'AverageDuration':{'$avg':'$time'}}}
        ]

        return self.collection.aggregate(pipeline=pipe)


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
    c = ClientMongo()
    print c.getAllAvgUpload()
    print c.getAllAvgDownload()
    # c.collection.insert(test)