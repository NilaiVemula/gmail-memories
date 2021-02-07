import functools
import json
import os

import flask
from flask import render_template, redirect
from authlib.integrations.requests_client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import gmail_auth

app = flask.Flask(__name__)
app.secret_key = '!secret'

app.register_blueprint(google_auth.app)
app.register_blueprint(gmail_auth.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        return flask.render_template('list.html', user_info=google_auth.get_user_info())

    return render_template('root.html')


@app.route('/emails')
def emails():
    labels = gmail_auth.get_emails()
    return labels


if __name__ == '__main__':
    app.run()
