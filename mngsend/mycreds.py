#!/usr/bin/env python
import os
import sys
import logging
import json

#from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as Request
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(format='%(asctime)-15s\t%(process)d:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

scopes = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.insert',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
]

# oauth2
#cred_file_oauth2 = 'mn/client_id.json'
cred_file_oauth2 = 'client_secret.json'
# https://stackoverflow.com/questions/62846906/httperror-400-precondition-check-failed-during-users-messages-list-gmail-api
# https://developers.google.com/identity/protocols/oauth2/service-account#authorizingrequests

token_file = 'gmail.token'

def _new_creds():
    ka = {'filename': cred_file, 'scopes': scopes}
    creds = Credentials.from_service_account_file(**ka)
    if not creds.token:
        creds.refresh(Request())

        # again
        if not creds.token:
            raise Exception('Could not refresh credentials')

    return creds


def _new_creds_2():
    flow = InstalledAppFlow.from_client_secrets_file(cred_file_oauth2, scopes)
    creds = flow.run_console()
    return creds


def _save_creds(creds):
    with open(token_file, 'w') as f:
        f.write(creds.to_json())

def get_creds(nonew=True):
    if os.path.exists(token_file):
        #print(dir(Credentials))
        with open(token_file) as f:
            creds = Credentials.from_authorized_user_info(json.load(f), scopes)
        #creds = Credentials.from_authorized_user_file(token_file, scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                creds = _new_creds_2()

            _save_creds(creds)

    else:
        if nonew:
            raise Exception('Not allowed to re-new creds')

        creds = _new_creds_2()
        _save_creds(creds)

    return creds

def main():
    get_creds()

if __name__ == '__main__':
    sys.exit(main())
