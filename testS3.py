from boto.s3.key import Key
import provider
import boto
from boto.s3.connection import S3Connection, Location

__author__ = 'antoine'


def deleteFile(bucket, cle):
    print 'Delete du bucket'
    bucket.delete_key(cle)


def uploadFile(nomFichier, nomCle, nomBucket):
    print 'Upload du fichier'
    b = getConnexion().get_bucket(nomBucket)
    k = getKey(b)
    k.key = nomCle
    k.set_contents_from_filename(nomFichier)
    print 'Fin upload'


def downloadFile(bucket, cle, nouveauNomFichier):
    print 'Download du fichier'
    key_we_know_is_there = bucket.get_key(cle, validate=False)
    res = key_we_know_is_there.get_contents_to_filename(nouveauNomFichier)
    print 'Fin download'


def getConnexion():
    p = provider.Provider('amazon')
    return S3Connection(p.app_key, p.app_secret)


def getKey(cle):
    return Key(cle)


def creationBucket(nomBucket, locationGeo):
    b = getConnexion()
    return b.create_bucket(nomBucket, location=locationGeo)


if __name__ == '__main__':
    print 'main S3'
    nomBucket = 'mdicbucket2015'
    cleBucket = 'testFichier01'
    nomFichier = 'working-draft.txt'
    # b = creationBucket(nomBucket,Location.EU)
    uploadFile(nomFichier, cleBucket, nomBucket)
    downloadFile(getConnexion().get_bucket(nomBucket), cleBucket, nomFichier)
    deleteFile(getConnexion().get_bucket(nomBucket), cleBucket)
