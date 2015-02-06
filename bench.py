#!venv/bin/python

import tempfile
from pprint import pformat
import datetime
import sys

import os
import dropbox
from execo import Timer
from execo_engine import Engine, sweep, ParamSweeper, igeom, slugify, logger
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import providerGD
import providerS3
import providerDB

from optparse import OptionParser
import requests


def cb(option, opt_str, value, parser):
        args = []
        for arg in parser.rargs:
                if arg[0] != "-":
                        args.append(arg)
                else:
                        del parser.rargs[:len(args)]
                        break
        if getattr(parser.values, option.dest):
                args.extend(getattr(parser.values, option.dest))
        setattr(parser.values, option.dest, args)

def getLocalisation():
    r = requests.get('http://ip-api.com/json/')

    if r.status_code == 200:
        content = r.json()
        return {'ip':content['query'],'lat':str(content['lat']),'lon':str(content['lon']),'city':str(content['city']),'country':str(content['country'])}
    else:
        p = requests.get('http://www.telize.com/geoip?callback=getgeoip')
        if r.status_code == 200:
            content = p.json()
            return {'ip':content['ip'],'lat':str(content['latitude']),'lon':str(content['longitude']),'city':str(content['city']),'country':str(content['country'])}
        else:
            return None

class Bench(Engine):
    """  """

    def __init__(self):
        super(Bench, self).__init__()

        self.options_parser.add_option('-s', '--size', dest='size', help='Size of the test', type=int)
        self.options_parser.add_option('-o', '--only', dest='only', help='Test only this size of the test', action='store_true', default=False)
        self.options_parser.add_option('-p', '--protocol', dest='protocol', choices=['sdk', 'rest', 'all'], default='all')
        self.options_parser.add_option('-n', '--ntest', dest='ntest', help='Number of tests', default=10)
        self.options_parser.add_option('-m', '--premium', dest='premium', help='Account used is premium',action='store_true', default=False)
        self.options_parser.add_option('-f', '--file', dest='file', metavar="FILE", help='File to test', default=False)
        self.options_parser.add_option('-t', '--transfert', dest='transfert', choices=['inter', 'upload','download','upDown'], default='upDown')
        self.options_parser.add_option('-d', '--drive', callback=cb, action='callback', dest='drive')
        self.options_parser.add_option('-a', '--all', action='store_true', dest='driveAll')
        self.options,self.args = self.options_parser.parse_args()

        if self.options.driveAll:
            self.drive = ['amazon','dropbox','googledrive']

        if self.options.transfert:
            self.transfert = ['upload','download']

        if self.options.size is None and self.options.file is False:
            print 'You have to give us a size or give us a file'
            sys.exit()


        if not self.options.drive:
            if self.options.file:
                print 'You choose to do all tests with this file  ' + str(self.options.file)
            else:
                print 'You choose to do all tests with a random file of this size ' + str(self.options.size)
        else:
            print 'You choose to a specific tests on '+ str(self.options.drive)

        # sys.exit()

    def create_file(self, size):
        """ """
        fd, fname = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fout:
            fout.write(os.urandom(size))
        return fname

    def run(self):
        """ """

        localisation = getLocalisation()

        size = dict
        if not self.options.file:
            if not self.options.only:
                size = igeom(128, int(self.options.size), 5)
            else:
                size = {long(self.options.size)}
        else:
            statinfo = os.stat(self.options.file)
            size = {long(statinfo.st_size)}

        drive = None
        if self.options.drive:
            drive = self.options.drive
        else:
            drive = self.drive

        interface = ['rest', 'sdk']
        parameters = {'size': size,
                      'if': interface,
                      'drive': drive,
                      'transfert':self.transfert}

        p = None

        for n in range(0,int(self.options.ntest),1):
            combs = sweep(parameters)
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pathResults = os.getcwd() + '/Results/Bench' + date
            sweeper = ParamSweeper(pathResults + "/sweeps", combs)
            f = open(pathResults + '/results.txt', 'w')

            while len(sweeper.get_remaining()) > 0:
                # sort the parameters
                for i in interface:
                    for dr in drive:
                        for s in size:
                            comb = sweeper.get_next(filtr = lambda r: filter(lambda x: x['drive'] == dr and  x['size'] == s and x['if'] == i, r))
                            if not comb: continue

                            # start of the workflow
                            if comb['drive'] == 'amazon':
                                p = providerS3.ProviderS3()
                            elif comb['drive'] == 'dropbox':
                                p = providerDB.ProviderDB()
                            else:
                                p = providerGD.ProviderGD()

                            logger.info('Treating combination %s', pformat(comb))
                            comb_dir = pathResults + '/' + slugify(comb)
                            try:
                                os.mkdir(comb_dir)
                            except:
                                pass

                            if not self.options.file:
                                fname = self.create_file(comb['size'])
                            else:
                                fname = self.options.file

                            timer = Timer()

                            if comb['if'] == 'sdk':
                                if p.provider_name == "amazon":
                                    p.bucketKey += fname
                                    p.upload_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey, fname)
                                    up_time = timer.elapsed()
                                    p.download_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey
                                                        ,comb_dir+'/'+fname.split('/')[-1])
                                    dl_time = timer.elapsed() - up_time

                                    # delete le fichier chez Amazon
                                    p.delete_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey)

                                elif p.provider_name == "dropbox":
                                    client = p.getToken()
                                    p.upload_file_sdk(client, fname, fname.split('/')[-1])
                                    up_time = timer.elapsed()
                                    p.download_file_sdk(client, fname.split('/')[-1],
                                                        comb_dir + '/' + fname.split('/')[-1])
                                    dl_time = timer.elapsed() - up_time

                                    # delete le fichier chez Dropbox
                                    client.file_delete(fname.split('/')[-1])

                                elif p.provider_name == "googledrive":
                                    drive_service = p.getConnexion()
                                    new_file = p.upload_file_sdk(drive_service, fname, fname.split('/')[-1], 'text/plain', 'desc')
                                    up_time = timer.elapsed()
                                    p.download_file_sdk(drive_service, new_file,comb_dir+'/'+fname.split('/')[-1])
                                    dl_time = timer.elapsed() - up_time

                                    # delete le fichier chez Google drive
                                    p.delete_file_sdk(drive_service, new_file['id'])

                                sweeper.done(comb)
                            elif comb['if'] == 'rest':
                                logger.warning('REST interface not implemented')
                                sweeper.skip(comb)
                                continue
                            f.write("%s %s %s %s %s %s %s %f %i %f %f\n" % (localisation['ip'],
                                                                            localisation['lat'],
                                                                            localisation['lon'],
                                                                            localisation['city'],
                                                                            localisation['country'],
                                                                            comb['drive'],
                                                                            comb['if'],
                                                                            timer.start_date(),
                                                                            comb['size'],
                                                                            up_time,
                                                                            dl_time))
                            os.remove(fname)
            f.close()
        os.rmdir(self.result_dir)


if __name__ == "__main__":
    e = Bench()
    e.start()