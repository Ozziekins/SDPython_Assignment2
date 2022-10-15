import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path


def auth_decorator(func):
    """
    The decorator helps to fetch authentication
    credentials and pass it to the function it's
    decorating
    :param func: The function to be guarded
    :return: the result of  the funciton
    """

    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive.readonly']
    secret_path = (Path(__file__).parent / '../../../assets/client_secrets.json').resolve()
    token_path = (Path(__file__).parent / '../../../assets/token.json').resolve()

    def wrapper(*args, **kwargs):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    secret_path, scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(secret_path, 'w') as token:
                token.write(creds.to_json())

        return func(creds, *args, **kwargs)

    return wrapper
