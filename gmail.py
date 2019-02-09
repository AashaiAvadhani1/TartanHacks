from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors
from bs4 import BeautifulSoup


def ridSpaces(listObjectEmail):
    for object in listObjectEmail:
        if(len(object) == " "):
            listObjectEmail.remove(object)




#PreCondition: a list of dictionaries with parts of an email
#PostCondition: string of the subject of an email
def findSetWithSubject(listDictionaries):
    for setObject in listDictionaries:
        for keySet in setObject:
            value = setObject[keySet]
            if(value == "Subject"):
                subjectName = findSubjectName(setObject)
                return subjectName

#PreCondition: a dictionary that contains values of the email components (DICT)
#PostCondition: the subject name (STR)
def findSubjectName(dictionaryObject):
    for key in dictionaryObject:
        value = dictionaryObject[key]
        #then we have reached the value case
        if(key == "value"):
            return dictionaryObject[key]




def GetMimeMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                     format='raw').execute()

        print('Message snippet: %s' % message['body'])
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except(errors.HttpError, error):
        print ('An error occurred: %s' % error)



def getEmailData():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    listOfMessages = []
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    #getting the thread messages from email
    threads = service.users().messages().list(userId = "me").execute()
    threads1 = threads["messages"]
    listDecode = []


    #get the name of the subject line (should be under headers then name)
    for thread in threads1:
        msg_id = thread["id"]
        message = service.users().messages().get(userId="me", id=msg_id, format='full').execute()
        try:
            listParts = [part for part in message["payload"]["parts"] if (part["mimeType"] == 'text/html')]
            for element in listParts:
                decode = base64.urlsafe_b64decode(element["body"]["data"])
                titleName = message["payload"]["headers"]
                subjectName = findSetWithSubject(titleName)
                stringOfDecode = str(decode)
                msg = BeautifulSoup(stringOfDecode,"lxml")
                #listDecode.append(stringOfDecode)

                thing = msg.get_text()


                thing = "SUBJECTSTART+ " + thing + " +SUBJECTEND"
                listDecode.append(thing)
        except:
            pass
    print(len(listDecode))
    return listDecode

getEmailData()
