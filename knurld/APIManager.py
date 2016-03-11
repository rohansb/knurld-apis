import json
import requests
from datetime import datetime

import app_globals as g


class Consumer(object):

    def __init__(self, token):
        self._token = token
        self.consumer = None

    def upsert_consumer(self, payload, consumer_id=None):
        """
        TODO: convert it as per the following definition using consumer_id
        update or insert the app model
        :param
        payload (e.g. format) = {
            "gender": "M",
            "username": "theo",
            "password": "walcott"
        }
        consumer_id: an existing consumer_id
        :return: href for the created or updated consumer
        """

        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer " + str(self._token),
                   "Developer-Id": g.config['DEVELOPER_ID']
                   }

        url = g.config['URL_CONSUMERS']
        # if consumer_id:
        #    url += '/' + consumer_id

        response = requests.post(url, json=payload, headers=headers)
        self.consumer = json.loads(response.content).get('href')

        return self.consumer

    def get_consumer(self):

        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer " + str(self._token),
                   "Developer-Id": g.config['DEVELOPER_ID']
                   }

        url = g.config['URL_CONSUMERS']
        # if consumer_id:
        #    url += '/' + consumer_id

        response = requests.get(url, headers=headers)
        result = json.loads(response.content)

        # if you are getting multiple consumers in result
        if result.get('items'):
            for item in result.get('items'):
                print item.get('href')
            # set the first one from result to be the consumer for this result
            self.consumer = result.get('items')[0].get('href')
        else:
            print result.get('href')
            self.consumer = result.get('href')

        return self.consumer


class AppModeler(object):

    def __init__(self, token):
        self._token = token
        self.app_model = None

    @property
    def app_model_id(self):
        if self.app_model:
            return self.app_model.split('/')[-1]
        return None

    def upsert_app_model(self, payload, app_model_id=None):
        """
        TODO: convert it as per the following definition using app_model_id
        update or insert the app model
        :param
        payload (e.g. format) = {
                "vocabulary": ["boston", "chicago", "pyramid"],
                "verificationLength": 3,
                "enrollmentRepeats": 3
            }
        app_model_id: an existing app model
        :return: href for the created or updated app model
        """

        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer " + str(self._token),
                   "Developer-Id": g.config['DEVELOPER_ID']
                   }

        url = g.config['URL_APP_MODELS']
        # if app_model_id:
        #    url += '/' + app_model_id

        response = requests.post(url, json=payload, headers=headers)
        self.app_model = json.loads(response.content).get('href')

        return self.app_model

    def get_app_model(self, app_model_id=None):

        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer " + str(self._token),
                   "Developer-Id": g.config['DEVELOPER_ID']
                   }

        url = g.config['URL_APP_MODELS']
        # if app_model_id:
        #    url += '/' + app_model_id

        response = requests.get(url, headers=headers)
        result = json.loads(response.content)
        # if you are getting multiple app models in result
        if result.get('items'):
            for item in result.get('items'):
                print item.get('href')
            # set the first one from result to be the app-model for this result
            self.app_model = result.get('items')[0].get('href')
        else:
            print result.get('href')
            self.app_model = result.get('href')

        return self.app_model


class TokenGetter(object):
    """
    Makes sure you always get a valid token. Validates the current available token and renews it if it has expired
    """

    def __init__(self, token=None):
        self._token = token
        self._token_timestamp = datetime.now()

    def _is_valid_token(self, token):
        """
        checking the validity of token based on the time it was issued last
        """
        try:
            time_lapse = (datetime.now() - self._token_timestamp).total_seconds()
            # print('time_lapse: ' + str(time_lapse))
            if time_lapse < g.config['TOKEN_EXPIRES']:
                return True
            else:
                # print("Invalid token {} with timestamp {}".format(token, self._token_timestamp))
                return False
        except ValueError as e:
            print("Invalid token {} Details: {}".format(token, e))

        return False

    def __deprecated__is_valid_token_status(self):
        """
        TO BE OBSOLETE METHOD
        Brian: do not rely on the token status api as it is going to go obsolete
        """
        params = {'Host': g.config['HOST'],
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + str(self._token),
                  'Developer-Id': g.config['DEVELOPER_ID']
                  }

        response = requests.get(g.config['URL_TOKEN_STATUS'], params=params)
        return True if response.status_code == 200 else False

    def renew_access_token(self):

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': g.config['HOST']
                   }

        payload = {'client_id': g.config['CLIENT_ID'],
                   'client_secret': g.config['CLIENT_SECRET']
                   }

        response = requests.post(g.config['URL_ACCESS_TOKEN'], data=payload, headers=headers)
        self._token = json.loads(response.content).get('access_token')
        self._token_timestamp = datetime.now()

        return self._token

    def get_token(self):
        """
        caching the already fetched token for duration configed in TOKEN_EXPIRES before the token could be renewed again
        """
        # check the cached version of the token first
        self._token = g.region.get_or_create("this_hour_token", creator=self.renew_access_token,
                                             expiration_time=g.config['TOKEN_EXPIRES'],
                                             should_cache_fn=self._is_valid_token)
        return self._token
