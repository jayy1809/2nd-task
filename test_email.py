import os
import base64
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.config.settings import settings
import asyncio

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = settings.GCD_CREDENTIALS_JSON_PATH

# The email of the user you are impersonating (must have delegated domain-wide authority)
DELEGATED_USER_EMAIL = "jaypanchal1809@gmail.com" # 'user@example.com'


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

async def create_gmail_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    # Delegate authority to the specified user
    credentials = credentials.with_subject(DELEGATED_USER_EMAIL)
    
    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=credentials)
    return service

async def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

async def send_email(sender, to, subject, message_text):
    try:
        service = await create_gmail_service()
        
        message = await create_message(sender, to, subject, message_text)
        
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent! Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    sender = DELEGATED_USER_EMAIL
    to = 'jaypanchal1809@gmail.com'
    subject = 'Test Email'
    message_text = 'This is a test email sent using the Gmail API with a Service Account.'
    
    await send_email(sender, to, subject, message_text)

# Run the script
if __name__ == '__main__':
    asyncio.run(main())