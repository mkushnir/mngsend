#!/usr/bin/env python
import os
import sys
import json
import logging
import base64
import email.mime.text

from googleapiclient.discovery import build

from . import mycreds

logging.basicConfig(format='%(asctime)-15s\t%(process)d:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

def main():
    subject = sys.argv[1]

    if len(sys.argv) >= 2:
        text = sys.argv[2]
    else:
        text = None
    if not text:
        text = sys.stdin.read()

    creds = mycreds.get_creds()
    gmail = build('gmail', 'v1', credentials=creds)

    msg = email.mime.text.MIMEText(text)
    msg['from'] = 'markiyan.kushnir@gmail.com'
    msg['to'] = 'markiyan_kushnir@yahoo.com'
    msg['cc'] = 'markiyan.kushnir@ukr.net'
    msg['subject'] = subject
    result = gmail.users().messages().send(userId='me', body={
        'raw': base64.urlsafe_b64encode(msg.as_string().encode('utf-8')).decode('utf-8')
    }).execute()

    logger.info('Sent: message id {id} thread {threadId} '
                'labels {labelIds}'.format(**result))



if __name__ == '__main__':
    sys.exit(main())

