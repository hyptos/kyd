from boto.s3.connection import S3Connection
from boto.s3.key import Key

__author__ = 'antoine'

import ConfigParser, os

class Provider():
    """ Object to store the provider ids """

    def __init__(self,providerName):
        """Load the provider's ids

        Args:
            providerName : Name of the drive (ex : dropbox, googledrive,...).
        """
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))
        self.provider_name = providerName
        self.app_key = config.get(providerName, 'app_key', 0)
        self.app_secret = config.get(providerName, 'app_secret', 0)
        self.token = config.get(providerName, 'token', 0)

class ProviderS3(Provider) :
    """ Object to store the provider ids """

    def __init__(self):
        """Load the provider's ids

        Args:
        """

        Provider.__init__(self,'amazon')
        self.bucketName = 'mdicbucket2015'
        self.bucketKey = 'mdicbucket2015_'

    def getConnexion(self):
        """Log an instance for S3.

        Args:.

        Returns:
        connection instance of S3  if successful, None otherwise.
        """
        return S3Connection(self.app_key, self.app_secret)


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

