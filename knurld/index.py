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
from knurldOauthClient import *
import json

app = flask.Flask(__name__)

# TODO place this in config
app.secret_key = "kramer"
users = {'kramer': 'knurld', 'elaine': 'knurld', 'jerry': 'knurld', 'geroge': 'knurld'}


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

                boss = Admin()
                if not boss.ouath_voice_verification_is_happy():
                    flask.flash("Audio verification Failed!")
            else:
                flask.flash("Audio verification file is required!")
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))


class Admin(flask.views.MethodView):

    @staticmethod
    def ouath_voice_verification_is_happy():

        client = OAuthClient(SERVER, PORT, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTHORIZATION_URL)
        consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
        signature_method_plaintext = oauth.OAuthSignatureMethod_PLAINTEXT()
        pause()

        # get request token
        print('* Obtain a request token ...')
        pause()
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            consumer, callback=CALLBACK_URL, http_url=client.request_token_url)
        oauth_request.sign_request(signature_method_plaintext, consumer, None)
        print('REQUEST (via headers)')
        print('parameters: %s' % str(oauth_request.parameters))
        pause()
        token = client.fetch_request_token(oauth_request)
        print('GOT')
        print('key: %s' % str(token.key))
        print('secret: %s' % str(token.secret))
        print('callback confirmed? %s' % str(token.callback_confirmed))
        pause()

        print('* Authorize the request token ...')
        pause()
        oauth_request = oauth.OAuthRequest.from_token_and_callback(
            token=token, http_url=client.authorization_url)
        print('REQUEST (via url query string)')
        print('parameters: %s' % str(oauth_request.parameters))
        pause()

        # this will actually occur only on some callback
        response = client.authorize_token(oauth_request)
        print('GOT')
        print(response)

        # is there a better way to get the verifier? not sure
        query = urlparse.urlparse(response)[4]
        params = urlparse.parse_qs(query, keep_blank_values=False)
        verifier = params['oauth_verifier'][0]
        print('verifier: %s' % verifier)
        pause()

        # only verification created for 'elaine benes'
        global RESOURCE_URL
        RESOURCE_URL = 'https://api.knurld.io/v1/verifications/a67a3f337823e2d56ec264f8c30c9375'
        response = client.access_resource(oauth_request)
        if response:
            doc = json.dumps(response)
            if doc['consumer']['username'] == 'elaine':
                return True

        return False


class Voices(flask.views.MethodView):
    @login_required
    def get(self):
        voices = ['http://www.soundboards.ws/data/sounds/368.mp3',
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

    app.debug = True
    app.run()
