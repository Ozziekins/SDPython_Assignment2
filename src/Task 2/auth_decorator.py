import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def auth_decorator(func):
    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive.readonly']

    def wrapper(*args, **kwargs):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../../assets/token.json'):
            creds = Credentials.from_authorized_user_file('../../assets/token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../../assets/client_secrets.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../../assets/token.json', 'w') as token:
                token.write(creds.to_json())

        return func(creds, *args, **kwargs)

    return wrapper
