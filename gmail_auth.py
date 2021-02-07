import io
import tempfile

import flask

from apiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import googleapiclient.discovery
from google_auth import build_credentials, get_user_info

from werkzeug.utils import secure_filename

app = flask.Blueprint('gmail_auth', __name__)


def build_gmail_api_v1():
    credentials = build_credentials()
    return googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

def get_emails():
    service = build_gmail_api_v1()

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


    return labels
