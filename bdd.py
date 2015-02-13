import ConfigParser
import datetime
from pymongo import MongoClient
import plotly.plotly as py
from plotly.graph_objs import *

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
            {
                '$group':{
                    '_id': {'drive' : "$drive", 'transfert':"$transfert", 'size':"$size"},'AverageDuration':{'$avg':'$time'}
                }
            },
            {
                '$sort':{
                    'size' : 1,
                    'AverageDuration':1
                }
            }
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
    print c.getAllAvgDownload()
    fd = open('all_result_download.txt','w')
    fu = open('all_result_upload.txt','w')
    for p in c.getAllAvgDownload()['result']:
        if p['_id']['transfert'] == "download":
            fd.write(p['_id']['drive'] + ' ' +  str(p['_id']['size']) + ' ' + str(p['AverageDuration']) + '\n' )
        else:
            fu.write(p['_id']['drive'] + ' ' +  str(p['_id']['size']) + ' ' + str(p['AverageDuration']) + '\n' )
    fd.close()
    fu.close()
