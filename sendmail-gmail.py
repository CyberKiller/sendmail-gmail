import ctypes
import sys
import pickle
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth import exceptions
import base64
from email.mime.text import MIMEText
from email.parser import BytesFeedParser
from apiclient import errors, discovery

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE_NAME = '.gmail_credentials.json'


def init_gmail(config):
    """Gets a gmail service object.
    """
    TOKENPICKLE_FILE_NAME = '.gmail_token.pickle'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKENPICKLE_FILE_NAME):
        with open(TOKENPICKLE_FILE_NAME, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except exceptions.RefreshError:
                creds = create_creds_pickle(config)
        else:
            creds = create_creds_pickle(config)
        # Save the credentials for the next run
        set_windows_hidden_file(TOKENPICKLE_FILE_NAME, hidden=False)
        with open(TOKENPICKLE_FILE_NAME, 'wb') as token:
            pickle.dump(creds, token)
            set_windows_hidden_file(TOKENPICKLE_FILE_NAME)

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return encode_message(message)


def create_msg_from_source(message_source, to=None):
    message_source = message_source.encode('utf-8')
    parser = BytesFeedParser()
    parser.feed(message_source)
    message = parser.close()
    if to is not None:
        message.replace_header('To', to)
    return encode_message(message)


def encode_message(message):
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: ' + message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: ' + str(error))
        
def create_creds_pickle(config):
    set_windows_hidden_file(CREDENTIALS_FILE_NAME, hidden=False)
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE_NAME, SCOPES)
    set_windows_hidden_file(CREDENTIALS_FILE_NAME)
    if config['console_oauth']:
        return flow.run_console()
    else:
        return flow.run_local_server()


def set_windows_hidden_file(filename, hidden = True):
    # https://stackoverflow.com/questions/25432139/python-cross-platform-hidden-file
    # Just Windows things
    if os.name != 'nt': return
    if not os.path.isfile(filename): return
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    INVALID_FILE_ATTRIBUTES = -1
    FILE_ATTRIBUTE_HIDDEN = 2
    FILE_ATTRIBUTE_UNHIDE = ~FILE_ATTRIBUTE_HIDDEN
    attrs = kernel32.GetFileAttributesW(filename)
    try:
        if attrs == INVALID_FILE_ATTRIBUTES:
            raise ctypes.WinError(ctypes.get_last_error())
        if hidden:
            attrs |= FILE_ATTRIBUTE_HIDDEN
        else:
            attrs &= FILE_ATTRIBUTE_UNHIDE
        if not kernel32.SetFileAttributesW(filename, attrs): 
            raise ctypes.WinError(ctypes.get_last_error())
    except OSError as e:
        print(f'Could not set file attributes for "{filename}". Error returned: ' + str(e))

CONFIG_FILE_NAME = 'config.json'

def get_config():
    try:
        with open(CONFIG_FILE_NAME, 'r') as f:
            return json.load(f)
    except Exception as e:
        print('Error reading config file. Error returned: ' + str(e))
        return False

def main():
    config = get_config()
    if config:
        to = config['rewrite_to']
    else:
        to = None

    if len(sys.argv) > 1: #if there are arguments
        files=sys.argv[1:]
        for f in files:
            send_message(init_gmail(config), 'me', create_msg_from_source(open(f).read(), to))
    else: #read from stdin
        send_message(init_gmail(config), 'me', create_msg_from_source(sys.stdin.read(), to))

if __name__ == '__main__':
    main()
