import apiclient
from execo_engine import logger
import httplib2
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors
from provider import Provider
import simplejson


class ProviderGD(Provider):
    """ Object to store the provider ids """

    def upload_file_sdk(self, service, filePath, fileName, fileType):
        """Upload a file's content.

        Args:
            service: Drive API service instance.
            filePath : Path to the file you want to upload.
            fileName : Name of the new file in the drive.
            fileType : Type of the file (text, ...)
            fileDescription : A short text to describe the file.

        Returns:
            File uploaded.
        """

        media_body = apiclient.http.MediaFileUpload(
            filePath,
            mimetype=fileType,
            resumable=True
        )
        body = {
            'title': fileName,
            'description': 'Temporary file',
        }
        new_file = None
        try:
            new_file = service.files().insert(body=body, media_body=media_body).execute()
        except errors.HttpError as e:
            error = simplejson.loads(e.content)
            logger.error('Error in Upload ' + error.get('code') + error.get('message'))
        return new_file


    def download_file_sdk(self, service, drive_file, pathFile):
        """Download a file's content.

        Args:
            service: Drive API service instance.
            drive_file: Drive File instance.

        Returns:
            File if successful, None otherwise.
        """
        if drive_file:
            download_url = drive_file.get('downloadUrl')
        else:
            download_url = self.retrieve_file_metadata(service, pathFile.split('/')[-1])
        if download_url:
            try:
                resp, content = service._http.request(download_url)
                if resp.status == 200:
                    out = open(pathFile, 'wb')
                    out.write(content)
                    out.close()
                    return out
            except errors.HttpError as e:
                error = simplejson.loads(e.content)
                logger.error('Error in Download ' + error.get('code') + error.get('message'))
        else:
            # The file doesn't have any content stored on Drive.
            return None

    def retrieve_file_metadata(self, service, fname):
        """Retrieve a list of File resources.

        Args:
        service: Drive API service instance.
        Returns:
        List of File resources.
        """
        result = []
        page_token = None
        while True:
            try:
                param = {'maxResults': 1, 'q': "title = '" + fname + "'"}
                if page_token:
                    param['pageToken'] = page_token

                files = service.files().list(**param).execute()
                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                logger.error('An error occurred: ' + error)
                break
            print result
            return result[0]['downloadUrl']


    def __init__(self):
        """Init the connexion to Google Drive.

        A credentials file is used to store the token and to renew it.

        Returns:
            The drive service.
        """

        Provider.__init__(self, 'googledrive')

    def getConnexion(self):

        # OAuth 2.0 scope that will be authorized.
        OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
        CRED_FILENAME = 'credentials'

        ### For storing token
        storage = Storage(CRED_FILENAME)
        if not storage.get():
            # Run through the OAuth flow and retrieve authorization code
            flow = OAuth2WebServerFlow(self.app_key, self.app_secret, OAUTH2_SCOPE, 'urn:ietf:wg:oauth:2.0:oob')
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            storage.put(credentials)
        else:
            # Getting access_token,expires_in,token_type,Refresh_toke info from CRED_FILENAME to 'credentials'
            credentials = storage.get()

        http = httplib2.Http()
        credentials.authorize(http)
        drive_service = build('drive', 'v2', http=http)
        return drive_service


    def delete_file_sdk(self, service, file_id):
        """Permanently delete a file, skipping the trash.

        Args:
            service: Drive API service instance.
            file_id: ID of the file to delete.
        """
        try:
            service.files().delete(fileId=file_id).execute()
        except errors.HttpError as e:
            error = simplejson.loads(e.content)
            logger.error('Error in delete ' + error.get('code') + error.get('message'))

