import ConfigParser

import dropbox
from provider import Provider
import requests
from dropbox.client import ErrorResponse
from execo_engine import logger


class ProviderDB(Provider):
    """ Object to store the provider ids """

    def upload_file_sdk(self, client, filePath, fileName):
        """Upload a file's content.
            Args:
                service: Drive API service instance.
                filePath : Path to the file you want to upload.
                fileName : Name of the new file in the drive.
            """
        f = open(filePath, 'rb')
        try:
            response = client.put_file(fileName, f)
        except ErrorResponse as e:
            logger.warning('Error in Upload ' + str(e.status) + ' ' + e.reason + ' : ' + e.error_msg)
            pass
        return True

    def download_file_sdk(self, client, fileName, filePath):
        """Download a file's content.
        Args:
            client: Dropbox client instance.
            fileName: Name of the file you want to download.
            filePath: Name of the new local file.
        """
        try:
            f, _ = client.get_file_and_metadata(fileName)
            out = open(filePath, 'wb')
            out.write(f.read())
            out.close()
        except ErrorResponse as e:
            logger.warning('Error in Download ' + str(e.status) + ' ' + e.reason + ' : ' + e.error_msg)
            pass
        return True

    def getNewToken(self):
        """ Get a new token for a new app """
        Provider.__init__(self, 'dropbox')
        print 'test de connexion a ' + self.provider_name
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        r = requests.get(flow.start())
        if r.status_code == 200:
            print "url:", flow.start()
            print "Please authorize in the browser. After you're done, press enter."
            auth_code = raw_input().strip()
            access_token, user_id = flow.finish(auth_code)
            config = ConfigParser.ConfigParser()
            config.readfp(open('conf.ini'))
            config.set('dropbox', 'token', access_token)
        else:
            return False
        return True

    def delete_file(self, client, fname):
        try:
            client.file_delete(fname)
        except ErrorResponse as e:
            logger.warning('Error in Delete ' + str(e.status) + ' ' + e.reason + ' : ' + e.error_msg)
            pass
        return True


    def getToken(self):
        if not self.token:
            self.getNewToken()
        return dropbox.client.DropboxClient(self.token)

    def __init__(self):
        """Init the connexion to Dropbox.

        Returns:
        The Dropbox client.
        """
        Provider.__init__(self, 'dropbox')
        self.getToken()
