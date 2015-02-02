import ConfigParser
import dropbox
from provider import Provider
import requests


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
            response = client.put_file(fileName, f)
            return response

    def download_file_sdk(self, client, fileName, filePath):
        """Download a file's content.
        Args:
            client: Dropbox client instance.
            fileName: Name of the file you want to download.
            filePath: Name of the new local file.
        """
        f, _ = client.get_file_and_metadata(fileName)
        out = open(filePath, 'wb')
        out.write(f.read())
        out.close()
        return True

    def getNewToken(self):
        """ Get a new token for a new app """
        Provider.__init__(self,'dropbox')
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

    def __init__(self):
        """Init the connexion to Dropbox.

        Returns:
        The Dropbox client.
        """
        Provider.__init__(self,'dropbox')
        if not self.token:
            self.getNewToken()
        return dropbox.client.DropboxClient(self.token)