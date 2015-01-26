from boto.s3.key import Key
import provider
import boto
from boto.s3.connection import S3Connection, Location

__author__ = 'antoine'

p = provider.Provider('amazon')
conn = S3Connection(p.app_key, p.app_secret)

# Choix de la location possible et creation du bucket
# conn.create_bucket('mdicbucket2015', location=Location.EU)
#  upload du fichier
b = conn.get_bucket('mdicbucket2015')
k = Key(b)
k.key = 'testText10k_01'
k.set_contents_from_filename('working-draft.txt')

# download le fichier
key_we_know_is_there = b.get_key('testText10k_01', validate=False)
res = key_we_know_is_there.get_contents_to_filename(key_we_know_is_there.testText10k_01)

# delete le bucket
conn.delete_bucket('mdicbucket2015')