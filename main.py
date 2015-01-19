from BeautifulSoup import BeautifulSoup
import requests

__author__ = 'antoine'

import unittest
import dropbox
import provider


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
        print client.account_info()
        self.assertTrue(len(client.account_info()) >= 3)


if __name__ == '__main__':
    unittest.main()
