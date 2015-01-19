__author__ = 'antoine'

import ConfigParser, os

class Provider():
    def __init__(self,providerName):
        config = ConfigParser.ConfigParser()
        config.readfp(open('conf.ini'))
        self.provider_name = providerName
        self.app_key = config.get(providerName, 'app_key', 0)
        self.app_secret = config.get(providerName, 'app_secret', 0)
        self.token = config.get(providerName, 'token', 0)
