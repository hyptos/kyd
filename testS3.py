from boto.s3.key import Key
import provider
import boto
from boto.s3.connection import S3Connection, Location

__author__ = 'antoine'


def deleteFile(bucket, key):
    """Delete a file on S3.

    Args:
    bucket: bucket instance.
    key: Key to delete.

    Returns:
    None.
    """
    bucket.delete_key(key)


def uploadFile(fileName, keyName, bucketName):
    """Upload a file to a specific bucket with a specific KeyName.

    Args:
    bucketName: name of the bucket where the file will be stored.
    keyName: Key where we store the file
    fileName: Name of the file on S3.

    Returns:
    None.
    """
    b = getConnexion().get_bucket(bucketName)
    k = getKey(b)
    k.key = keyName
    k.set_contents_from_filename(fileName)


def downloadFile(bucket, key, newFileName):
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


def getConnexion():
    """Log an instance for S3.

    Args:.

    Returns:
    connection instance of S3  if successful, None otherwise.
    """
    p = provider.Provider('amazon')
    return S3Connection(p.app_key, p.app_secret)


def getKey(key):
    """return a Key for S3.

    Args:.
        key: key to return

    Returns:
    Key instance  if successful, None otherwise.
    """
    return Key(key)


def createBucket(bucketName, locationGeo):
    """Create a bucket on S3 for a zone.

    Args:.
        bucketName: name of the bucket
        locationGeo: enum of boto.Location

    Returns:
    Bucket instance if successful, None otherwise.
    """
    b = getConnexion()
    return b.create_bucket(bucketName, location=locationGeo)


if __name__ == '__main__':
    print 'main S3'
    nomBucket = 'mdicbucket2015'
    cleBucket = 'testFichier01'
    nomFichier = 'working-draft.txt'
    # b = createBucket(nomBucket,Location.EU)
    uploadFile(nomFichier, cleBucket, nomBucket)
    downloadFile(getConnexion().get_bucket(nomBucket), cleBucket, nomFichier)
    deleteFile(getConnexion().get_bucket(nomBucket), cleBucket)
