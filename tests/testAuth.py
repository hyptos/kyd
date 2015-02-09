import ConfigParser
import unittest
import providerDB
import providerGD
import providerS3


class testAuth(unittest.TestCase):

    #test if tokens are up
    def test_connexionGoogle(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))

        self.app_key = config.get('googledrive', 'app_key', 0)
        self.app_secret = config.get('googledrive', 'app_secret', 0)

        self.assertIsNotNone(self.app_key)
        self.assertIsNotNone(self.app_secret)


    def test_connexionDropboxToken(self):
        p = providerDB.ProviderDB()
        self.assertIsNotNone(p.getToken())



    def test_connexionS3(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))
        self.app_key = config.get('amazon', 'app_key', 0)
        self.app_secret = config.get('amazon', 'app_secret', 0)

        self.assertIsNotNone(self.app_key)
        self.assertIsNotNone(self.app_secret)

    def test_connexionS3Token(self):
        p = providerS3.ProviderS3()
        self.assertIsNotNone(p.getConnexion())

    def test_connexionDropbox(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))
        self.app_key = config.get('dropbox', 'app_key', 0)
        self.app_secret = config.get('dropbox', 'app_secret', 0)

        self.assertIsNotNone(self.app_key)
        self.assertIsNotNone(self.app_secret)

    def test_connexionGoogleToken(self):
        p = providerGD.ProviderGD()
        self.assertIsNotNone(p.getConnexion())




if __name__ == '__main__':
    unittest.main()
