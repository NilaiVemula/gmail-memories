from flask import Flask, render_template

import google_auth
import gmail

app = Flask(__name__)
app.secret_key = '!secret'

app.register_blueprint(google_auth.app)
app.register_blueprint(gmail.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        return render_template('success.html', user_info=google_auth.get_user_info())

    return render_template('index.html')


@app.route('/emails')
def emails():
    labels = gmail.get_emails()
    return "<p> got labels successfully! </p>"


if __name__ == '__main__':
    app.run()
