import json
import string
from urllib.error import HTTPError
from create_service import Create_Service
import os
import pandas as pd
import requests


spreadIdFile = open('spreadId.json')
spreadIdFile = json.load(spreadIdFile)



# Create_Service(client_secret_file, api_name, api_version, *scopes):
CLIENT_SECRET_FILE= 'credentials.json'
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/photoslibrary']

SPREADSHEET_ID = spreadIdFile['spreadId']
ID_COLUMN = 'C2:C'

print("the spreadsheet id is", SPREADSHEET_ID)
photoService = Create_Service(CLIENT_SECRET_FILE,API_SERVICE_NAME,API_VERSION,SCOPES,static_discovery=False)

API_SERVICE_NAME= 'sheets'
API_VERSION= 'v4'

sheetService = Create_Service(CLIENT_SECRET_FILE,API_SERVICE_NAME,API_VERSION,SCOPES,static_discovery=False)


headers= {
    "Content-type":"application/json"
}


sheet = sheetService.spreadsheets()


TEST_ALBUM_ID = photoService.albums().list().execute()['albums']['title'=='TEST ALBUM']['id']
# concatenate this to the base url to acces it in another application
# base-url=wmax-width-hmax-height

search = {
    "albumId":TEST_ALBUM_ID,
    "pageSize":25
}

images = []

# This block returns the array items full of the base urls for the images. 
testItems = photoService.mediaItems().search(body=search).execute()
items = testItems.get('mediaItems')
page = testItems.get('nextPageToken')

search['pageToken']=testItems['nextPageToken']

while(page):
    # search next page and extend items. use nextPageToken to find the next page. 
    nextPageOfItems = photoService.mediaItems().search(body=search).execute()
    page = nextPageOfItems.get('nextPageToken')
    search['pageToken']=page
    media = nextPageOfItems.get('mediaItems')
    items.extend(media)



idToUrl = {}


for item in items:
    if (not isinstance(item,str)):
        url = "(\"" + item['baseUrl'] + '=w2048-h2048' +"\")"
        urlWithFunction = "=IMAGE"+url
        # what format should the input be if I am updating a cell at a time?
        idToUrl[item['filename'].split('_')[1].split('.')[0]]=urlWithFunction




columnC = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range= ID_COLUMN).execute()
columnC = columnC.get('values')

for index,each in enumerate(columnC):

    columnC[index] = str(each[0])
    


def rangeFinder(arrayOfKeys,dictionary, columnLetter):
    flag= False
    start = None
    arrayRange=[]
    end = None
    for index, key in enumerate(arrayOfKeys, start = 2):
        if key in dictionary and flag == False:
            start = str(index)
            flag = True
        if key not in dictionary and flag == True:
            end = str(index -1);
            flag = False
            range = f'{columnLetter}{start}:{columnLetter}{end}'
            arrayRange.append(range)
    return arrayRange

validColumnCRanges = rangeFinder(arrayOfKeys=columnC, dictionary=idToUrl,columnLetter='C')
print(validColumnCRanges)

validColumnORanges = rangeFinder(arrayOfKeys=columnC,dictionary=idToUrl,columnLetter = 'O' )


batchUpdateDictionary= {}

columnCValueRange = sheet.values().batchGet(spreadsheetId = SPREADSHEET_ID,ranges = validColumnCRanges).execute()
# we get the valueRanges array of valueRange objects
arrayOfColumnC = columnCValueRange.get('valueRanges')



for index,valueRangeObject in enumerate(arrayOfColumnC):
    valueRangeObject['range']=validColumnORanges[index]


# array of column c is an array of value range objects. 
# within the value range objects are arrays of values. these values are single arrays containing keys 
# for each value range object for each value in object.values
# value[0]=idToUrl[value[0]]

for valRangeObject in arrayOfColumnC:
    for value in valRangeObject['values']:
        value[0]=idToUrl[value[0]]

print(arrayOfColumnC)
batchBody = {

    "valueInputOption":"USER_ENTERED",
    "data":arrayOfColumnC,
    "includeValuesInResponse":False
}
sheet.values().batchUpdate(spreadsheetId= SPREADSHEET_ID,body= batchBody).execute()
