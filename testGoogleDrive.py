import apiclient
import httplib2
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import provider
from apiclient import errors







if __name__ == '__main__':

    DESCRIPTION = 'A shiny new text document about lorem ipsum.'

    new_file = upload_file(drive_service, 'working-draft.txt', 'My New Text Document', 'text/plain', DESCRIPTION)

    download_file(drive_service, new_file)

    delete_file(drive_service, new_file['id'])
