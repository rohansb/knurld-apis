"""
Author: Rohan Bakare
Program: Intednted to access the knurld developer API services, and create a sample app for audio verification
"""

import flask
import flask.views
from flask_oauthlib.client import OAuth
from flask_oauthlib.provider import OAuth1Provider
import functools

app = flask.Flask(__name__)

# TODO place this in config
app.secret_key = "kramer"
users = {'kramer': 'knurld'}


class Main(flask.views.MethodView):
    @staticmethod
    def get():
        return flask.render_template('index.html')

    @staticmethod
    def post():
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'passwd']

        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))

        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("You required to login to see the page!")
            return flask.redirect(flask.url_for('index'))
    return wrapper


class Admin(flask.views.MethodView):

    oauth_client = OAuth()
    oauth_provider = OAuth1Provider(app)
    oauth_provider.init_app(app)

    # TODO: config it from a secured place
    oauth_dict = {'client_id': 'sfgpWaOrgNgLASXQGUQFMdZQA3NmZxG0',
                  'client_secret': 'wbjADuCttwnJx0nW'
                  }
    uri = {'access-token': 'https://api.knurld.io//oauth/client_credential/accesstoken?grant_type=client_credentials', }

    # register to the remote knurld apis
    knurld = oauth_client.remote_app(
        'knurld',
        base_url='https://api.knurld.io//',
        request_token_url=None,
        access_token_url='https://api.knurld.io//oauth/client_credential/accesstoken?grant_type=client_credentials',
        authorize_url=None,
        consumer_key=oauth_dict['client_id'],
        consumer_secret=oauth_dict['client_secret']
        )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "client_id": oauth_dict['client_id'],
        "consumer_secret": oauth_dict['client_secret'],
    }

    @knurld.tokengetter
    def get_knurld_token(self, token=None):
        # registering this function as a token getter
        return token

    @login_required
    def get(self):

        # r = requests.post(self.uri['access-token'], json=json.dumps(self.headers))

        r = self.get_knurld_token()
        app.logger.debug(r)

        return flask.render_template('admin.html')


    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('admin'))


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
