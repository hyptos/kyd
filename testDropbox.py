import json
import datetime
from BeautifulSoup import BeautifulSoup
import requests
import unittest
import dropbox
import provider
import timeit


def getNewToken():
    p = provider.Provider('dropbox')
    print 'test de connexion a ' + p.provider_name
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(p.app_key, p.app_secret)
    r = requests.get(flow.start())
    if r.status_code == 200:
        print "url:", flow.start()
        print "Please authorize in the browser. After you're done, press enter."
        auth_code = raw_input().strip()
        access_token, user_id = flow.finish(auth_code)
        print access_token


def init():
    p = provider.Provider('dropbox')
    return dropbox.client.DropboxClient(p.token)


def upload_file(client, filePath, fileName):
    # Upload the file
    f = open(filePath, 'rb')
    # nowUpload = datetime.datetime.now()
    response = client.put_file(fileName, f)
    #afterUpload = datetime.datetime.now()
    #diff = afterUpload - nowUpload
    #print "Upload time for 10k file " + diff.__str__()


def download_file(fileName):
    # Get the file
    # nowDownload = datetime.datetime.now()
    f, metadata = client.get_file_and_metadata('/testText10k_01.txt')
    #afterDownload = datetime.datetime.now()
    #diff = afterDownload - nowDownload
    #print "Download time for 10k file " + diff.__str__()
    out = open(fileName, 'wb')
    out.write(f.read())
    out.close()


if __name__ == '__main__':
    client = init()

    FILEPATH = 'working-draft.txt'
    FILENAME = '/testText10k_01.txt'

    upload_file(client, FILEPATH, FILENAME)

    download_file(FILENAME)

    response = client.file_delete(FILENAME)