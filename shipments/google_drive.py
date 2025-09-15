import os
import json
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

# Setup logging (Render will capture console logs)
logger = logging.getLogger(__name__)

# Load .env only in local mode
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Your Shared Drive folder ID (from your link)
DEFAULT_FOLDER_ID = "1KmlipO7ZnG-q7pUM-nNFyOgzWopgCzvR"
# If you know your Shared Drive ID, set it here (optional)
DEFAULT_DRIVE_ID = None  # e.g. "0Axxxxxxxxxxxxxxxxxxxx"

def get_drive_service():
    try:
        # Try from Render environment variable
        service_account_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

        if service_account_info:
            logger.info("Loading Google Drive creds from environment variable")
            info = json.loads(service_account_info)
            creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        else:
            # Local dev fallback
            CREDENTIALS_PATH = os.environ.get('GOOGLE_DRIVE_CLIENT_SECRET_PATH')
            logger.info(f"Loading Google Drive creds from file: {CREDENTIALS_PATH}")
            creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)

        return build('drive', 'v3', credentials=creds)

    except Exception as e:
        logger.error(f"Google Drive authentication failed: {e}", exc_info=True)
        raise

def upload_file_to_drive_path(file_path, filename=None, mimetype=None, folder_id=DEFAULT_FOLDER_ID, drive_id=DEFAULT_DRIVE_ID):
    """Upload a file from disk (file path) to the Shared Drive folder"""
    try:
        service = get_drive_service()
        file_metadata = {'name': filename or os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        if drive_id:
            file_metadata['driveId'] = drive_id

        media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink',
            supportsAllDrives=True
        ).execute()

        logger.info(f"Uploaded file {file.get('id')} → {file.get('webViewLink')}")
        return file.get('id'), file.get('webViewLink')

    except Exception as e:
        logger.error(f"Google Drive upload failed: {e}", exc_info=True)
        raise

def upload_file_to_drive_obj(file_obj, filename, mimetype=None, folder_id=DEFAULT_FOLDER_ID, drive_id=DEFAULT_DRIVE_ID):
    """Upload a file-like object (e.g., from Django admin) to the Shared Drive folder"""
    try:
        service = get_drive_service()
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        if drive_id:
            file_metadata['driveId'] = drive_id

        media = MediaIoBaseUpload(file_obj, mimetype=mimetype, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink',
            supportsAllDrives=True
        ).execute()

        logger.info(f"Uploaded file {file.get('id')} → {file.get('webViewLink')}")
        return file.get('id'), file.get('webViewLink')

    except Exception as e:
        logger.error(f"Google Drive upload failed: {e}", exc_info=True)
        raise