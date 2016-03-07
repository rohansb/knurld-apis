"""
Author: Rohan Bakare
Program: Intednted to access the knurld developer API services, and create a sample app for audio verification
Reference: https://github.com/jakecoffman/flask-tutorial/blob/master/part%203%20-%20login/demo.py
https://github.com/joestump/python-oauth2/blob/7d72ac16225a283f0fbf1d1ac6d1d7d20b3136c5/example/client.py

hosted .wav files:
 kramer: http://audiofiles2.jerryseinfeld.nl/kramer_theassman.wav (knurld verification-id: not created)
 elaine: http://audiofiles2.jerryseinfeld.nl/hooker.wav (knurld verification-id: a67a3f337823e2d56ec264f8c30c9375)
 jerry: http://audiofiles2.jerryseinfeld.nl/icaniple.wav (knurld verification-id: not created)

"""

import flask
import flask.views
from helpers import login_required
import httplib2

app = flask.Flask(__name__)

# TODO place this in config
app.secret_key = "kramer"
users = {'kramer': 'knurld', 'elaine': 'knurld', 'jerry': 'knurld', 'geroge': 'knurld'}
ACCESS_TOKEN_URL = 'https://api.knurld.io//oauth/client_credential/accesstoken?grant_type=client_credentials'


class Main(flask.views.MethodView):
    @staticmethod
    def get():
        return flask.render_template('index.html')

    @staticmethod
    def post():
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))

        required = ['username', 'passwd', 'audio_verification_file']
        for r in required:
            if not flask.request.form[r]:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))

        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        audio_verification_file = flask.request.form['audio_verification_file']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
            if audio_verification_file:
                flask.session['audio_verification_file'] = audio_verification_file

                # begin audio verification here
                boss = Admin()
                verified = boss.verify_user_based_on_the_audio(audio_verification_file)
                if not verified:
                    flask.flash("Username doesn't exist or incorrect password")
            else:
                flask.flash("Audio verification file is required!")
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))


class Admin(flask.views.MethodView):

    @staticmethod
    def get():
        return flask.render_template('admin.html')

    @staticmethod
    def post():
        return flask.render_template('admin.html')

    @staticmethod
    def verify_user_based_on_the_audio(audio_file):
        _verified = False

        # get the token
        #   - what is the simplest possible way?
        #       - use httplib2 -------- DONE
        #       - use urllib2 instead to do the same thing, because its the norm as being a better library:
        #           http://hustcalm.me/blog/2013/11/14/httplib-httplib2-urllib-urllib2-whats-the-difference/
        #

        #   - renew it every hour --------- IN-PROGRESS
        #   - make it as a decorator which can be used everywhere?

        http = httplib2.Http()

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = 'client_id=sfgpWaOrgNgLASXQGUQFMdZQA3NmZxG0&client_secret=wbjADuCttwnJx0nW'
        response, content = http.request(uri=ACCESS_TOKEN_URL, method='POST', body=body, headers=headers)

        print(content)

        return _verified


class Voices(flask.views.MethodView):
    @login_required
    def get(self):
        voices = [
                'http://audiofiles2.jerryseinfeld.nl/kramer_theassman.wav',
                'http://audiofiles2.jerryseinfeld.nl/hooker.wav',
                'http://audiofiles2.jerryseinfeld.nl/icaniple.wav',
                'http://www.soundboards.ws/data/sounds/368.mp3',
                'http://www.soundboards.ws/data/sounds/1/804.mp3',
                'http://www.soundboards.ws/data/sounds/1/391.mp3']

        return flask.render_template("voices.html", voices=voices)

app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/admin/',
                 view_func=Admin.as_view('admin'),
                 methods=['GET', 'POST'])
app.add_url_rule('/voices/',
                 view_func=Voices.as_view('voices'),
                 methods=['GET'])


if __name__ == '__main__':

    # app.debug = True
    # app.run()

    audio_verification_file = 'http://audiofiles2.jerryseinfeld.nl/kramer_theassman.wav'

    boss = Admin()
    verified = boss.verify_user_based_on_the_audio(audio_verification_file)
