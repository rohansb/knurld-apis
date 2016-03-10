import json


class Configuration(object):

    def __init__(self, max_expiration_time=3599):  # as per the APIs after every 3599 seconds current token expires
        self._config = None
        self._max_expiration_time = max_expiration_time

    @property
    def config(self):
        try:
            with open('config.cfg', 'r+') as cf:
                content = cf.read().replace('\r\n', '')
                self._config = json.loads(content)

                # Do the type checks and set appropriate types
                self._config['TOKEN_EXPIRES'] = float(self._config['TOKEN_EXPIRES'])

                # if the Token Expire time is greater than max allowable duration then reset it to max
                if self._config['TOKEN_EXPIRES'] > self._max_expiration_time:
                    self._config['TOKEN_EXPIRES'] = self._max_expiration_time

        except ValueError as e:
            print('Could not load the configuration! {}'.format(e))

        return self._config
