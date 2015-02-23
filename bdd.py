import ConfigParser
import datetime
import sys
from pymongo import MongoClient


class ClientMongo(object):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))

        PORT = int(config.get('mongo', 'MONGODB_PORT', 0))
        HOST = config.get('mongo', 'MONGODB_HOST', 0)
        self.client = MongoClient(HOST, PORT)
        self.db = self.client.kydDb
        self.collection = self.db.kyd

    def cleanBdd(self):
        self.collection.remove({})

    def getAllAvgUpload(self):
        pipe = [
            {'$group': {'_id': {'drive': "$drive", 'transfert': "upload"}, 'AverageDuration': {'$avg': '$time'}}}
        ]

        return self.collection.aggregate(pipeline=pipe)

    def getAllAvgDownload(self):
        pipe = [
            {
                '$group': {
                '_id': {'drive': "$drive", 'transfert': "$transfert", 'size': "$size",
                        'start_day': {'$dayOfMonth': "$start_date"}, 'start_hour': {'$hour': '$start_date'}},
                'AverageDuration': {'$avg': '$time'},
                'count': {'$sum': 1}
                }
            },
            {
                '$sort': {
                    'start_day': 1,
                    'start_hour': 1
                }
            }
        ]

        return self.collection.aggregate(pipeline=pipe)

    def checkExpExist(self,options):

        if options.driveAll:
            drive = ['amazon', 'dropbox', 'googledrive']
        else:
            drive = options.drive

        if len(options.transfert) == 1:
            if options.transfert == 'updown':
                transfert = ['download','upload']
            else:
                transfert = [options.transfert]
        else:
            transfert = ['download','upload']



        pipe = [
            {
                '$or':[
                    {
                        'day':'Lundi',
                        'city' :'Villeurbanne',
                        'drive': {'$in': drive},
                        'size' : options.size,
                        'transfert':{'$in': transfert}
                    }
                ]
            }
        ]
        print pipe
        #sys.exit()
        return self.collection.find(pipeline=pipe)


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
    'time': 2.22
}

if __name__ == "__main__":
    c = ClientMongo()

    fd = open('all_result_download.txt', 'w')
    for p in c.getAllAvgDownload()['result']:
        if str(p['_id']['start_day']) == '20' and str(p['_id']['start_hour']) >= '16' and str(p['_id']['transfert']) == 'download':
            print p
            fd.write(p['_id']['drive'] + ' ' + str(p['_id']['size']) + ' ' + str(p['AverageDuration']) + '\n')
    fd.close()
