from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import io
from apiclient import http as apiclent_http

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
PATH = os.path.dirname(os.path.abspath(__file__))
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = PATH+'/client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    home_dir = os.path.expanduser(PATH)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def file_list():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    result = {}
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=1000).execute()

    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        # print('Files:')
        for item in items:
            # print('{0} ({1})'.format(item['name'], item['id']))
            result.update({item['name']: item['id']})
    # print(result)
    return result


def get_fiel(file_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    # request = drive_service.files().get_media(fileId=file_id)
    request = drive_service.files().export_media(fileId=file_id,
                                                 mimeType='text/plain')
    fh = io.BytesIO()
    downloader = apiclent_http.MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        # print("Download %d%%." % int(status.progress() * 100))

    # print(fh.getvalue().decode('utf-8'))
    return fh.getvalue().decode('utf-8')


def get_doc_data(name):
    try:
        id = file_list()[name]
        data = get_fiel(id)
    except:
        print(name)
        print('未发现对应DOC ID')
        data = None
    return data


if __name__ == '__main__':
    print(file_list())
    # a = get_doc_data('all+发送后popup + 延长展示时长+长尾')
    # print(a)
