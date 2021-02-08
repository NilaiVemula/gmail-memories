
from flask import Blueprint
import json
from urllib.error import HTTPError
import googleapiclient.discovery
from googleapiclient.discovery_cache import base
from httplib2 import Http
from google_auth import build_credentials, get_user_info

import base64

from find_html import find_mime_type

app = Blueprint('gmail', __name__)


def build_gmail_api_v1():
    credentials = build_credentials()
    return googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)


def get_emails():
    service = build_gmail_api_v1()
    date_string = 'after:2020/02/05 before:2020/02/10'
    request = service.users().messages().list(userId='me', q=date_string)
    try:
        response = request.execute()
    except HTTPError as e:
        print('Error response status code : {0}, reason : {1}'.format(
            e.resp.status, e.error_details))

    messages = list(response["messages"])
    ids = [message["id"] for message in messages]

    data_to_display = []

    for id in ids:
        
        try:
            
            
            email = {}

            request = service.users().messages().get(userId='me', id=id)
            response = request.execute()

            # mime_type = "text/html"
            # try:
            #     key_chain = find_mime_type(response, mime_type)
            # except KeyError:
            #     print('Could not find this mime type: {0}'.format(mime_type))
            #     exit()
            # print('Found {0} mime type here: {1}'.format(mime_type, key_chain))
            # nested = response
            # for key in key_chain:
            #     nested = nested[key]
            # print('Confirmation lookup: {0}'.format(nested))

            
            
            
            
            headers = list(response["payload"]["headers"])
            
            looking_for = ["Date", "Subject", "From", "To"]
            for header in headers:
                if header["name"] in looking_for:
                    email[header["name"]] = header["value"]
                

            #email["Subject"] = response["payload"]["headers"][3]["value"]
            #email["From"] = response["payload"]["headers"][4]["value"]
            #email["To"] = response["payload"]["headers"][5]["value"]

            try:

                base64_message = response["payload"]["parts"][0]["parts"][0]["body"]["data"]
                
            except (KeyError, TypeError) as e:
                try:
                    base64_message = response["payload"]["parts"][0]["body"]["data"]
                except (KeyError, TypeError) as e:
                    base64_message = "Ti9B"
            email["body"] = base64.urlsafe_b64decode(
                base64_message).decode('utf-8')
        except HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.resp.status, e.error_details))

        data_to_display.append(email)

    return data_to_display
