from __future__ import print_function

import os.path

# os .path is the operating system path...where the computer looks for stuff.

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.photos','https://www.googleapis.com/auth/photoslibrary']

# The ID and range of a sample spreadsheet. 
SPREADSHEET_ID = '1YjruUegz018LabEyDxOjrDnXyO7Fkr-q_O5Muu-BOLE'
SAMPLE_RANGE_NAME = 'A1:E4'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        # creates...creds...using credentials object from oauth2 module.
        # if the token.json file is created that is. 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        
        # get method apparently populates an array(takes name of array and array as arguments)
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            print('%s, %s' % (row[0], row[1]))

        # write some values...
        sheet.values().update(spreadsheetId = SPREADSHEET_ID,range = SAMPLE_RANGE_NAME, valueInputOption="RAW", body = {"values":[[90,10,12]]}).execute()


        # put an image into a cell from google photos...
    except HttpError as err:
        print(err)
    finally:
        service.close()







if __name__ == '__main__':
    main()