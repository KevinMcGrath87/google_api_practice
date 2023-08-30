import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def Create_Service(client_secret_file, api_name, api_version, *scopes,static_discovery):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    STATIC_DISCOVERY= static_discovery
    print(SCOPES)

    cred = None

    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.json'
    # print(token_file)

    if os.path.exists(token_file):
            cred = Credentials.from_authorized_user_file(token_file,SCOPES)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port = 0)

        with open(token_file, 'w') as token:
            token.write(cred.to_json())

    try:
        print("starting build")
        print(cred)
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred,static_discovery=STATIC_DISCOVERY)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e,"error time!")
    return None

