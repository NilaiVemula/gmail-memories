
from flask import Blueprint
from urllib.error import HTTPError
import googleapiclient.discovery
from google_auth import build_credentials

import base64

from datetime import date, timedelta


app = Blueprint('gmail', __name__)


def build_gmail_api_v1():
    """generate the gmail api service"""

    credentials = build_credentials()
    return googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)


def get_emails():
    """find all emails from one year ago"""

    # generate the gmail api service
    service = build_gmail_api_v1()

    # compute date for one year ago
    today = date.today()
    one_year_ago = today - timedelta(days=365.25)
    start = one_year_ago - timedelta(days=1)
    end = one_year_ago + timedelta(days=1)
    start_string = start.strftime("%Y/%m/%d")
    end_string = end.strftime("%Y/%m/%d")
    query_string = f'after:{start_string} before:{end_string}'

    # generate the gmail api request (get list of messages from one year ago)
    request = service.users().messages().list(userId='me', q=query_string)

    # try to get the api response
    try:
        response = request.execute()
    except HTTPError as e:
        print('Error response status code : {0}, reason : {1}'.format(
            e.resp.status, e.error_details))

    # get list of message ids from the api response
    messages = list(response["messages"])
    ids = [message["id"] for message in messages]

    # store all emails in a list
    data_to_display = []

    # loop through each message id
    for id in ids:

        try:
            # store email data in a dict
            email = {}

            # get message data by querying gmail api using message id
            request = service.users().messages().get(userId='me', id=id)
            response = request.execute()

            # get date, subject, from, to, etc from message header
            headers = list(response["payload"]["headers"])
            looking_for = ["Date", "Subject", "From", "To"]
            for header in headers:
                if header["name"] in looking_for:
                    email[header["name"]] = header["value"]

            # try to get message body (base64) from response
            # the json structure varies a lot so that is why there are no many try/except
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

            # decode the email body
            email["body"] = base64.urlsafe_b64decode(
                base64_message).decode('utf-8')

            # populate list with email
            data_to_display.append(email)

        except HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.resp.status, e.error_details))

    return data_to_display
