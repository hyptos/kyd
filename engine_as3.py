#!/usr/bin/env python

import tempfile
from pprint import pformat

import os
import provider
from execo import Timer
from execo_engine import Engine, sweep, ParamSweeper, igeom, slugify, logger
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class S3Bench(Engine):
    """  """

    def create_file(self, size):
        """ """
        fd, fname = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fout:
            fout.write(os.urandom(size))
        return fname


    def getConnexion(self):
        """Log an instance for S3.

        Args:.

        Returns:
        connection instance of S3  if successful, None otherwise.
        """
        p = provider.Provider('amazon')
        return S3Connection(p.app_key, p.app_secret)


    def getKey(self, key):
        """return a Key for S3.

        Args:.
            key: key to return

        Returns:
        Key instance  if successful, None otherwise.
        """
        return Key(key)

    def download_file_sdk(self, bucket, key, newFileName):
        """Download a file and save it.

        Args:
        bucket: bucket instance.
        key: Drive File instance.
        newFileName: Name of the file.

        Returns:
        File if successful, None otherwise.
        """
        key_we_know_is_there = bucket.get_key(key, validate=False)
        return key_we_know_is_there.get_contents_to_filename(newFileName)

    def upload_file_sdk(self, bucketName, keyName, fileName):
        """Upload a file to a specific bucket with a specific KeyName.

        Args:
        bucketName: name of the bucket where the file will be stored.
        keyName: Key where we store the file
        fileName: Name of the file on S3.

        Returns:
        None.
        """
        b = self.getConnexion().get_bucket(bucketName)
        k = self.getKey(b)
        k.key = keyName
        k.set_contents_from_filename(fileName)

    def delete_file_sdk(self, bucket, key):
        """Delete a file on S3.

        Args:
        bucket: bucket instance.
        key: Key to delete.

        Returns:
        None.
        """
        bucket.delete_key(key)

    def createBucket(self, bucketName, locationGeo):
        """Create a bucket on S3 for a zone.

        Args:.
            bucketName: name of the bucket
            locationGeo: enum of boto.Location

        Returns:
        Bucket instance if successful, None otherwise.
        """
        b = self.getConnexion()
        return b.create_bucket(bucketName, location=locationGeo)


    def run(self):
        """ """
        p = provider.Provider('amazon')
        nomBucket = 'mdicbucket2015'

        parameters = {'size': igeom(128, 2048, 5),
                      's3_if': ['rest', 'sdk']}
        combs = sweep(parameters)
        sweeper = ParamSweeper(self.result_dir + "/sweeps", combs)

        f = open(self.result_dir + '/results.txt', 'w')
        f.write("timer_start\t\tsize\tupload_time\tdownload_time\n")
        while len(sweeper.get_remaining()) > 0:
            comb = sweeper.get_next()

            logger.info('Treating combination %s', pformat(comb))
            comb_dir = self.result_dir + '/' + slugify(comb)
            try:
                os.mkdir(comb_dir)
            except:
                pass

            fname = self.create_file(comb['size'])

            timer = Timer()

            if comb['s3_if'] == 'sdk':
                cleBucket = 'mdicbucket2015_' + fname
                self.upload_file_sdk(self.getConnexion().get_bucket(nomBucket), cleBucket, fname)
                up_time = timer.elapsed()
                self.download_file_sdk(self.getConnexion().get_bucket(nomBucket), cleBucket
                                       ,comb_dir+'/'+fname.split('/')[-1])
                dl_time = timer.elapsed() - up_time

                # delete le fichier chez Dropbox
                self.delete_file_sdk(self.getConnexion().get_bucket(nomBucket), cleBucket)

                sweeper.done(comb)
            elif comb['s3_if'] == 'rest':
                logger.warning('REST interface not implemented')
                sweeper.skip(comb)
                continue
            os.remove(fname)
            f.write("%f\t%i\t%f\t%f\n" % (timer.start_date(), comb['size'], up_time, dl_time))
        f.close()


if __name__ == "__main__":
    e = S3Bench()
    e.start()