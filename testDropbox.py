import ConfigParser
import json
import datetime
from BeautifulSoup import BeautifulSoup
import requests
import unittest
import dropbox
import provider
import timeit


def getNewToken():
    """ Get a new token for a new app """
    p = provider.Provider('dropbox')
    print 'test de connexion a ' + p.provider_name
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(p.app_key, p.app_secret)
    r = requests.get(flow.start())
    if r.status_code == 200:
        print "url:", flow.start()
        print "Please authorize in the browser. After you're done, press enter."
        auth_code = raw_input().strip()
        access_token, user_id = flow.finish(auth_code)
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))
        config.set('dropbox', 'token', access_token)


def init():
    """Init the connexion to Dropbox.

    Returns:
        The Dropbox client.
    """
    p = provider.Provider('dropbox')
    if not p.token:
        getNewToken()
    return dropbox.client.DropboxClient(p.token)


def upload_file(client, filePath, fileName):
    """Upload a file's content.

    Args:
        service: Drive API service instance.
        filePath : Path to the file you want to upload.
        fileName : Name of the new file in the drive.
    """

    f = open(filePath, 'rb')
    response = client.put_file(fileName, f)


def download_file(client, fileName, filePath):
    """Download a file's content.

    Args:
        client: Dropbox client instance.
        fileName: Name of the file you want to download.
        filePath: Name of th new local file.
    """
    f, metadata = client.get_file_and_metadata(filePath)
    out = open(fileName, 'wb')
    out.write(f.read())
    out.close()


if __name__ == '__main__':
    client = init()

    FILEPATH = 'working-draft.txt'
    FILENAME = '/testText10k_01.txt'

    nowUpload = datetime.datetime.now()
    upload_file(client, FILEPATH, FILENAME)
    afterUpload = datetime.datetime.now()
    diff = afterUpload - nowUpload
    print "Upload time for 10k file " + diff.__str__()

    nowDownload = datetime.datetime.now()
    download_file(client, FILENAME, FILENAME)
    afterDownload = datetime.datetime.now()
    diff = afterDownload - nowDownload
    print "Download time for 10k file " + diff.__str__()

    response = client.file_delete(FILENAME)