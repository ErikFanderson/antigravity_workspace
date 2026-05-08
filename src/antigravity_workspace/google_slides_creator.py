import os
import json
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Default Paths (relative to repo root)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_DIR = os.path.join(REPO_ROOT, "credentials/google")
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, "token.json")

def get_services():
    """Initializes Google Slides and Drive services."""
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"Token not found at {TOKEN_PATH}. Please ensure you have authenticated.")
        
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)
    
    creds = Credentials.from_authorized_user_info(token_data)
    slides_service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return slides_service, drive_service

def create_presentation(slides_service, title):
    """Creates a new Google Slides presentation."""
    presentation = slides_service.presentations().create(body={'title': title}).execute()
    presentation_id = presentation.get('presentationId')
    print(f'Created presentation: "{title}" (ID: {presentation_id})')
    return presentation_id

def upload_image_to_drive(drive_service, file_path, name="uploaded_image.png"):
    """Uploads an image to Drive and returns a public URL for Slides API."""
    file_metadata = {'name': name}
    media = MediaFileUpload(file_path, mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    
    # Set public permission so Slides API can access the image URL
    drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
    
    return f'https://drive.google.com/uc?export=view&id={file_id}'

def add_title_slide(slides_service, presentation_id, title, subtitle):
    """Updates the default first slide with title and subtitle."""
    presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
    slide = presentation['slides'][0]
    title_id = slide['pageElements'][0]['objectId']
    subtitle_id = slide['pageElements'][1]['objectId']
    
    requests = [
        {'insertText': {'objectId': title_id, 'text': title}},
        {'insertText': {'objectId': subtitle_id, 'text': subtitle}},
        # Styling: Dark theme
        {
            'updatePageProperties': {
                'objectId': slide['objectId'],
                'pageProperties': {
                    'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 0.1, 'green': 0.1, 'blue': 0.3}}}}
                },
                'fields': 'pageBackgroundFill.solidFill.color'
            }
        },
        {'updateTextStyle': {'objectId': title_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}}}, 'fields': 'foregroundColor'}},
        {'updateTextStyle': {'objectId': subtitle_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}}}}, 'fields': 'foregroundColor'}}
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()

def add_content_slide(slides_service, presentation_id, title, body_text):
    """Adds a standard TITLE_AND_BODY slide."""
    requests = [{'createSlide': {'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}}}]
    response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()
    slide_id = response['replies'][0]['createSlide']['objectId']
    
    presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
    slide = next(s for s in presentation['slides'] if s['objectId'] == slide_id)
    
    title_placeholder = next(e['objectId'] for e in slide['pageElements'] if 'shape' in e and e['shape']['placeholder'].get('type') == 'TITLE')
    body_placeholder = next(e['objectId'] for e in slide['pageElements'] if 'shape' in e and e['shape']['placeholder'].get('type') == 'BODY')
    
    content_requests = [
        {'insertText': {'objectId': title_placeholder, 'text': title}},
        {'insertText': {'objectId': body_placeholder, 'text': body_text}},
        {
            'updatePageProperties': {
                'objectId': slide_id,
                'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 0.95, 'green': 0.95, 'blue': 1.0}}}}},
                'fields': 'pageBackgroundFill.solidFill.color'
            }
        }
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': content_requests}).execute()

def find_presentations(drive_service, name):
    """Finds presentations by name."""
    query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.presentation' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def list_presentations(drive_service):
    """Lists all presentations in Drive."""
    query = "mimeType = 'application/vnd.google-apps.presentation' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def main():
    parser = argparse.ArgumentParser(description="Create Google Slides presentations.")
    parser.add_argument("--title", default="New Presentation", help="Title of the presentation")
    args = parser.parse_args()

    slides_service, drive_service = get_services()
    print("Google API services initialized.")
    # For now, this script serves as a library/template. 
    # Logic for specific presentations can be added here or in separate scripts.

if __name__ == "__main__":
    main()
