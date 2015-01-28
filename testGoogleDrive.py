import apiclient
import googleapiclient
import pprint
import httplib2
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import provider
from apiclient import errors


def init():
    """Init the connexion to Google Drive.

    A credentials file is used to store the token and to renew it.

    Returns:
        The drive service.
    """

    p = provider.Provider('googledrive')

    # OAuth 2.0 scope that will be authorized.
    OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
    CRED_FILENAME = 'credentials'

    ### For storing token
    storage = Storage(CRED_FILENAME)
    if not storage.get():
        # Run through the OAuth flow and retrieve authorization code
        flow = OAuth2WebServerFlow(p.app_key, p.app_secret, OAUTH2_SCOPE, 'urn:ietf:wg:oauth:2.0:oob')
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


def upload_file(service, filePath, fileName, fileType, fileDescription):
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

    MIMETYPE = 'text/plain'
    TITLE = 'My New Text Document'
    DESCRIPTION = 'A shiny new text document about lorem ipsum.'

    media_body = apiclient.http.MediaFileUpload(
        filePath,
        mimetype=fileType,
        resumable=True
    )
    body = {
        'title': fileName,
        'description': fileDescription,
    }

    new_file = service.files().insert(body=body, media_body=media_body).execute()

    return new_file


def download_file(service, drive_file):
    """Download a file's content.

    Args:
        service: Drive API service instance.
        drive_file: Drive File instance.

    Returns:
        File if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
            print 'Status: %s' % resp
            out = open('testText10k_02.txt', 'wb')
            out.write(content)
            out.close()
            return out
        else:
            print 'An error occurred: %s' % resp
            return None
    else:
        # The file doesn't have any content stored on Drive.
        return None


def delete_file(service, file_id):
    """Permanently delete a file, skipping the trash.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to delete.
    """
    try:
        service.files().delete(fileId=file_id).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


if __name__ == '__main__':
    drive_service = init()

    DESCRIPTION = 'A shiny new text document about lorem ipsum.'

    new_file = upload_file(drive_service, 'working-draft.txt', 'My New Text Document', 'text/plain', DESCRIPTION)

    download_file(drive_service, new_file)

    delete_file(drive_service, new_file['id'])
