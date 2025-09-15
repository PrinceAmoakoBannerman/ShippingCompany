import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SCOPES = ['https://www.googleapis.com/auth/drive.file']

CREDENTIALS_PATH = os.environ.get('GOOGLE_DRIVE_CLIENT_SECRET_PATH')
TOKEN_PATH = os.environ.get('GOOGLE_DRIVE_TOKEN_PATH')

# Debug: show resolved paths and existence (handles missing env safely)
print("CREDENTIALS_PATH:", CREDENTIALS_PATH)
print("TOKEN_PATH:", TOKEN_PATH)
print("Does credentials file exist?", bool(CREDENTIALS_PATH and os.path.exists(CREDENTIALS_PATH)))
print("Does token file exist?", bool(TOKEN_PATH and os.path.exists(TOKEN_PATH)))

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive_path(file_path, filename=None, mimetype=None, folder_id=None):
    """Upload a file from disk (file path)"""
    service = get_drive_service()
    file_metadata = {'name': filename or os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file.get('id'), file.get('webViewLink')

def upload_file_to_drive_obj(file_obj, filename, mimetype=None, folder_id=None):
    """Upload a file-like object (e.g., from Django admin)"""
    service = get_drive_service()
    file_metadata = {'name': filename}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaIoBaseUpload(file_obj, mimetype=mimetype, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file.get('id'), file.get('webViewLink')