from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth_decorator import auth_decorator


@auth_decorator
def get_file_id(creds, file_name):
    folder_id = '1nfrYxDm7TLzls9pedZbLX5rP4McVDWDe'

    def list_files():
        list_of_files = []

        query = f"'{folder_id}' in parents and name='{file_name}'"

        # Get list of jpg files in shared folder
        page_token = None

        while True:
            response = service.files().list(
                q=query,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()

            for file in response.get('files', []):
                list_of_files.append(file)

            page_token = response.get('nextPageToken', None)
            if page_token is None or len(list_of_files) > 0:
                break

        return list_of_files

    service = build('drive', 'v3', credentials=creds)
    try:
        files = list_files()
        if len(files) == 0:
            return None
        elif len(files) == 1:
            return files[0]['id']
        else:
            raise Exception

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}');
