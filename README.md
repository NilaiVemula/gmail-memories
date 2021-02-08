# Gmail Memories

**Author:** Nilai Vemula

**Goal:** Allow a user to log in with gmail and show them a list of emails they received from exactly one year ago

**Date:** 2/6/2021 - 2/7/2021

[Live Version on Heroku](https://gmail-memories.herokuapp.com/)

<hr>

## What is it?

Gmail Memories is a fun, little tool that allows you to log-in and it will show you a list of emails you received a year ago. Think of it as Google Photos Memories but for Gmail.

## How does it work?

Gmail Memories is a Flask App. When you first access the website, you are able to login through Google. All authentication is handled in `google_auth.py`, and I use the `authlib` library. The permissions on authentication require access to all Gmail messages and settings, but no data is ever stored permanently. The `googleapiclient` library is used for generating API requests to the Gmail API. Finally, the data is aggregated and displayed to the user using a basic [HTML template](templates/emails.html).

## How can it be better?

Ideally, this would be like Google Photos and this would show up directly in your inbox. For that, maybe I could build a Google Chrome extension, but this Flask app will suffice for now. The design is basic HTML, but it isn't horribly ugly, other than the `iframe` elements I use to display the email content. The JSON response from the Gmail API also has variable structure, so I am not guaranteed to get the email content. I still have to come up with a better way of parsing the JSON data. Finally, because of how Google handles its API, the service is in test mode and it is **invite-only**.

## Developer details

In order to get this project up and running on your local machine, you will first need to set up a new project on the Google Cloud Platform and generate credentials (Client ID and Client Secret) that you will save as environment variables. Next, you will have to generate a Flask secret key that will also be saved as an environment variable. Finally, you can clone the repository and generate a Python 3.9 virtual environment with the necessary dependencies from `requirements.txt`. The flask app can be run using the command `python app.py`.
