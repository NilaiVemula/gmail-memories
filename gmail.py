
from flask import Blueprint
import json
from urllib.error import HTTPError
import googleapiclient.discovery
from googleapiclient.discovery_cache import base
from httplib2 import Http
from google_auth import build_credentials, get_user_info

import base64

from datetime import date, datetime, timedelta


app = Blueprint('gmail', __name__)


def build_gmail_api_v1():
    credentials = build_credentials()
    return googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)


def get_emails():
    service = build_gmail_api_v1()

    today = date.today()
    one_year_ago = today - timedelta(days=365.25)
    start = one_year_ago - timedelta(days=1)
    end = one_year_ago + timedelta(days=1)
    start_string = start.strftime("%Y/%m/%d")
    end_string = end.strftime("%Y/%m/%d")
    query_string = f'after:{start_string} before:{end_string}'
    request = service.users().messages().list(userId='me', q=query_string)
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

            headers = list(response["payload"]["headers"])

            looking_for = ["Date", "Subject", "From", "To"]
            for header in headers:
                if header["name"] in looking_for:
                    email[header["name"]] = header["value"]

            try:

                base64_message = response["payload"]["parts"][0]["parts"][0]["body"]["data"]

            except (KeyError, TypeError) as e:
                try:
                    base64_message = response["payload"]["parts"][1]["body"]["data"]
                except (KeyError, TypeError, IndexError) as e:
                    try:
                        base64_message = response["payload"]["parts"][0]["body"]["data"]
                    except (KeyError, TypeError, IndexError) as e:
                        try:
                            base64_message = response["payload"]["body"]["data"]
                        except (KeyError, TypeError, IndexError) as e:
                            base64_message = "Ti9B"
            email["body"] = base64.urlsafe_b64decode(
                base64_message).decode('utf-8')
        except HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.resp.status, e.error_details))

        data_to_display.append(email)

    return data_to_display
