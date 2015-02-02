#!/usr/bin/env python

import tempfile
from pprint import pformat

import os
import dropbox
from execo import Timer
from execo_engine import Engine, sweep, ParamSweeper, igeom, slugify, logger
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import providerGD
import providerS3
import providerDB


class Bench(Engine):
    """  """

    def __init__(self):
        super(Bench, self).__init__()

        self.options_parser.add_option('-s', '--size', dest='size', help='size of the test', type=int)
        self.options_parser.add_option('-o', '--only', dest='only', type=bool, help='test only this size of the test', default=False)
        self.options_parser.add_option('-p', '--protocol', dest='protocol', choices=['sdk', 'rest', 'all'], default='all')
        self.options_parser.add_option('-m', '--premium', dest='premium', type=bool, help='Account used is premium', default=False)
        self.options_parser.add_option('-f', '--file', dest='file', metavar="FILE", help='file to test', default=False)
        self.options_parser.add_option('-t', '--transfert', dest='transfert', choices=['inter', 'upload','download','upDown'], default='upDown')
        self.options_parser.add_option('-c', '--cloud', dest='cloud', choices=['dropbox', 'amazon', 'googledrive', 'all'], default='all')

        print 'arg de size: ' + str(self.options.size)
        print 'arg de only: ' + str(self.options.only)
        print 'arg de protocol: ' + str(self.options.protocol)
        print 'arg de transfert: ' + str(self.options.transfert)
        print 'arg de file: ' + str(self.options.file)
        print 'arg de cloud: ' + str(self.options.cloud)

        if self.options.size is None and self.options.file is False:
            print 'You have to give us a size or give us a file'
            #sys.exit()

        print 'You choose to do all tests with a random file of ' + str(self.options.size)



    def create_file(self, size):
        """ """
        fd, fname = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fout:
            fout.write(os.urandom(size))
        return fname

    def run(self):
        """ """
        if self.options.cloud == 'amazon':
            p = providerS3.ProviderS3()
        elif self.options.cloud == 'dropbox':
            p = providerDB.ProviderDB()
        elif self.options.cloud == 'googledrive':
            p = providerGD.ProviderGD()

        parameters = {'size': igeom(128, 2048, 5),
                      'if': ['rest', 'sdk']}
        combs = sweep(parameters)
        nomBench = p.provider_name
        sweeper = ParamSweeper(nomBench + "/sweeps", combs)

        f = open(nomBench + '/results.txt', 'w')
        while len(sweeper.get_remaining()) > 0:
            comb = sweeper.get_next()

            logger.info('Treating combination %s', pformat(comb))
            comb_dir = nomBench + '/' + slugify(comb)
            try:
                os.mkdir(comb_dir)
            except:
                pass

            fname = self.create_file(comb['size'])

            timer = Timer()

            if comb['if'] == 'sdk':
                if p.provider_name == "amazon":
                    p.bucketKey += fname
                    p.upload_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey, fname)
                    up_time = timer.elapsed()
                    p.download_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey
                                           ,comb_dir+'/'+fname.split('/')[-1])
                    dl_time = timer.elapsed() - up_time

                    # delete le fichier chez Dropbox
                    p.delete_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey)

                elif p.provider_name == "dropbox":
                    client = dropbox.client.DropboxClient(p.token)
                    self.upload_file_sdk(client, fname, fname.split('/')[-1])
                    up_time = timer.elapsed()
                    self.download_file_sdk(client, fname.split('/')[-1],
                                           comb_dir + '/' + fname.split('/')[-1])
                    dl_time = timer.elapsed() - up_time

                    # delete le fichier chez Dropbox
                    client.file_delete(fname.split('/')[-1])

                elif p.provider_name == "googledrive":
                    drive_service = self.init()
                    new_file = self.upload_file_sdk(drive_service, fname, fname.split('/')[-1], 'text/plain', 'desc')
                    up_time = timer.elapsed()
                    self.download_file_sdk(drive_service, new_file)
                    dl_time = timer.elapsed() - up_time

                    # delete le fichier chez Dropbox
                    self.delete_file_sdk(drive_service, new_file['id'])

                sweeper.done(comb)
            elif comb['if'] == 'rest':
                logger.warning('REST interface not implemented')
                sweeper.skip(comb)
                continue
            os.remove(fname)
            f.write("%f %i %f %f\n" % (timer.start_date(), comb['size'], up_time, dl_time))
        f.close()


if __name__ == "__main__":
    e = Bench()
    e.start()