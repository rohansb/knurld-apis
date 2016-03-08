import json


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

