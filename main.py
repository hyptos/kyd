import json
import datetime
from BeautifulSoup import BeautifulSoup
import requests

__author__ = 'antoine'

import unittest
import dropbox
import provider
import timeit

class TestConnexionFunctions(unittest.TestCase):
    # def test_connexionDropbox(self):
    #     p = provider.Provider('dropbox')
    #     print 'test de connexion a ' + p.provider_name
    #     flow = dropbox.client.DropboxOAuth2FlowNoRedirect(p.app_key, p.app_secret)
    #     r = requests.get(flow.start())
    #     if r.status_code == 200:
    #         print "url:", flow.start()
    #         print "Please authorize in the browser. After you're done, press enter."
    #         auth_code = raw_input().strip()
    #         access_token, user_id = flow.finish(auth_code)
    #         print access_token
    #     self.assertTrue(r.status_code == 200)

    def test_connexionDropboxWithToken(self):
        p = provider.Provider('dropbox')
        client = dropbox.client.DropboxClient(p.token)
        self.assertTrue(len(client.account_info()) >= 3)

    def test_sendFileDropbox(self):

        # Upload the file
        p = provider.Provider('dropbox')

        client = dropbox.client.DropboxClient(p.token)
        f = open('working-draft.txt', 'rb')
        nowUpload = datetime.datetime.now()
        response = client.put_file('/testText10k_01.txt', f)
        afterUpload = datetime.datetime.now()
        diff = afterUpload - nowUpload
        print "Upload time for 10k file " + diff.__str__()


        # Get the file
        nowDownload = datetime.datetime.now()
        f, metadata = client.get_file_and_metadata('/testText10k_01.txt')
        afterDownload = datetime.datetime.now()
        diff = afterDownload - nowDownload
        print "Download time for 10k file " + diff.__str__()

        out = open('testText10k_01.txt', 'wb')
        out.write(f.read())
        out.close()

        response = client.file_delete('/testText10k_01.txt')
        self.assertTrue(response['is_deleted'])

if __name__ == '__main__':
    unittest.main()
