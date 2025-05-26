from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import datetime
import os
import re

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_unread_emails():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat() + 'Z'
    results = service.users().messages().list(userId='me', q=f'is:unread after:{yesterday}').execute()
    messages = results.get('messages', [])
    email_data = []
    keywords = ["interview", "assessment", "phone interview", "technical interview", "offer", "invitation", "job", "application status"]
    app_keywords = ["application submitted", "job application", "application received", "your application was sent", "thank you for applying"]

    application_count = 0

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt['payload']
        headers = payload.get('headers')
        subject = sender = ''
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']

        body = ''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                    data = part['body']['data']
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    clean_text = re.sub('<[^<]+?>', '', html_body)
                    body += clean_text
        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        body = re.sub(r'\s+', ' ', body.strip())
        combined_text = (subject + " " + body).lower()

        # Count job application emails
        if any(keyword in combined_text for keyword in app_keywords):
            application_count += 1

        # Filter for interview/assessment emails
        if any(keyword in combined_text for keyword in keywords):
            email_data.append(f"From: {sender}\nSubject: {subject}\nBody: {body}\n\n")

    return email_data, application_count
