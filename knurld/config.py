import json
import requests
from datetime import datetime
from dogpile.cache import make_region


class Configuration(object):

    def __init__(self):
        self._config = None

    @property
    def config(self):
        try:
            with open('config.cfg', 'r+') as cf:
                content = cf.read().replace('\r\n', '')
                self._config = json.loads(content)
        except ValueError as e:
            print('Could not load the configuration! {}'.format(e))

        return self._config


class TokenGetter(object):
    """
    Makes sure you always get a valid token. Validates the current available token and renews it if it has expired
    """

    def __init__(self, token=None):
        self._token = token
        self._token_timestamp = datetime.now()
        self.config = Configuration().config
        self.region = make_region().configure('dogpile.cache.memory',
                                              expiration_time=self.config['TOKEN_EXPIRES_IN'],
                                              )

    def _is_valid_token(self, token):
        """
        checking the validity of token based on the time it was issued last
        """
        try:
            time_lapse = (datetime.now() - self._token_timestamp).total_seconds()
            print('time_lapse: ' + str(time_lapse))
            if float(time_lapse) < float(self.config['TOKEN_EXPIRES_IN']):
                return True
            else:
                return False
        except ValueError as e:
            print("Invalid token timestamp {}".format(e))

        return False

    def __deprecated__is_valid_token_status(self):
        """
        OBSOLETE METHOD
        Brian: do not rely on the token status api as it is going to go obsolete
        """
        headers = {'Host': self.config['DEVELOPER_ID'],
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + str(self._token),
                   'Developer-Id': self.config['DEVELOPER_ID']
                   }

        response = requests.get(self.config['TOKEN_STATUS_URL'], params=headers)
        return True if response.status_code == 200 else False

    def renew_access_token(self):

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': self.config['HOST']}

        payload = {'client_id': self.config['CLIENT_ID'],
                   'client_secret': self.config['CLIENT_SECRET']
                   }

        response = requests.post(self.config['ACCESS_TOKEN_URL'], data=payload, headers=headers)
        self._token = json.loads(response.content).get('access_token')
        self._token_timestamp = datetime.now()

        return self._token

    def get_token(self):
        """
        caching the already fetched token for 3569 (just less than an hour, value configed in TOKEN_EXPIRES_IN)
        before the token could be renewed again
        """

        print('timestamp1: ' + str(self._token_timestamp))
        print('_is_valid_token: ' + str(self._is_valid_token(self._token)))

        # check the cached version of the token first
        self._token = self.region.get_or_create("this_hour_token", creator=self.renew_access_token,
                                                expiration_time=self.config['TOKEN_EXPIRES_IN'],
                                                should_cache_fn=self._is_valid_token)
        print('timestamp2: ' + str(self._token_timestamp))

        return self._token
