#!/usr/bin/env python

import tempfile
from pprint import pformat

import os
import provider
from execo import Timer
from execo_engine import Engine, sweep, ParamSweeper, igeom, slugify, logger
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class Bench(Engine):
    """  """

    def create_file(self, size):
        """ """
        fd, fname = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fout:
            fout.write(os.urandom(size))
        return fname

    def run(self):
        """ """
        p = provider.ProviderS3()

        parameters = {'size': igeom(128, 2048, 5),
                      'if': ['rest', 'sdk']}
        combs = sweep(parameters)
        nomBench = p.provider_name
        sweeper = ParamSweeper(nomBench + "/sweeps", combs)

        f = open(nomBench + '/results.txt', 'w')
        f.write("timer_start\t\tsize\tupload_time\tdownload_time\n")
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
                p.bucketKey += fname
                p.upload_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey, fname)
                up_time = timer.elapsed()
                p.download_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey
                                       ,comb_dir+'/'+fname.split('/')[-1])
                dl_time = timer.elapsed() - up_time

                # delete le fichier chez Dropbox
                p.delete_file_sdk(p.getConnexion().get_bucket(p.bucketName), p.bucketKey)

                sweeper.done(comb)
            elif comb['if'] == 'rest':
                logger.warning('REST interface not implemented')
                sweeper.skip(comb)
                continue
            os.remove(fname)
            f.write("%f\t%i\t%f\t%f\n" % (timer.start_date(), comb['size'], up_time, dl_time))
        f.close()


if __name__ == "__main__":
    e = Bench()
    e.start()