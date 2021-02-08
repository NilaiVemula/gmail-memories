from flask import Flask, render_template

import google_auth
import gmail
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

app.register_blueprint(google_auth.app)
app.register_blueprint(gmail.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        return render_template('success.html', user_info=google_auth.get_user_info())

    return render_template('index.html')


@app.route('/emails')
def emails():
    email_data = gmail.get_emails()
    return render_template('emails.html', emails=email_data)


if __name__ == '__main__':
    app.run()
