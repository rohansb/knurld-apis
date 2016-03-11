import unittest
from datetime import datetime, timedelta

from APIManager import TokenGetter, AppModeler, Consumer


class TestEnrollment(unittest.TestCase):
    pass


class TestConsumer(unittest.TestCase):

    tg = TokenGetter()
    token = tg.get_token()
    c = Consumer(token)

    def test_upsert_consumer(self):

        payload = {
            "gender": "M",
            "username": "theo" + str(datetime.now()),   # making sure of unique username each time
            "password": "walcott"
        }

        consumer = self.c.upsert_consumer(payload, self.token)
        consumer_pattern = '.*knurld.*consumers\/\w{32}'

        self.assertRegexpMatches(consumer, consumer_pattern)

    def test_get_consumer(self):
        consumer = self.c.get_consumer()
        consumer_pattern = '.*knurld.*consumers\/\w{32}'

        self.assertRegexpMatches(consumer, consumer_pattern)


class TestAppModeler(unittest.TestCase):

    tg = TokenGetter()
    token = tg.get_token()
    am = AppModeler(token)

    def test_upsert_app_model(self):

        payload = {
            "vocabulary": ["boston", "chicago", "pyramid"],
            "verificationLength": 3,
            "enrollmentRepeats": 3
        }

        # TODO: currently the upsert method can only create an app model, so modify this test when it method evolves
        app_model = self.am.upsert_app_model(payload)
        app_model_pattern = '.*knurld.*app-models\/\w{32}'

        self.assertRegexpMatches(app_model, app_model_pattern)

    def test_get_app_model(self):
        app_model = self.am.get_app_model()
        app_model_pattern = '.*knurld.*app-models\/\w{32}'

        self.assertRegexpMatches(app_model, app_model_pattern)


class TestTokenGetter(unittest.TestCase):

    tg = TokenGetter()

    def test_renew_access_token(self):

        # new token must be the one just got fetched using remote APIs
        token = self.tg.renew_access_token()
        self.assertEqual(self.tg._token, token)

    def test_is_valid_token(self):

        # set up for an unexpired token (assuming self.tg object is created just a moments ago, this is a valid token)
        is_valid = self.tg._is_valid_token(self.tg._token)
        self.assertEqual(True, is_valid)

        # set up for an expired token
        self.tg._token_timestamp = datetime.now() - timedelta(seconds=3600)

        # the current token may or may not be valid based on the tg timestamp
        is_valid = self.tg._is_valid_token(self.tg._token)
        self.assertEqual(False, is_valid)

    def test_get_token(self):
        # set up for an expired token
        cur_token = self.tg._token
        new_token = self.tg.get_token()
        self.assertNotEqual(cur_token, new_token)

        # set up for an unexpired token (assuming self.tg object is created just a moments ago, this is a valid token)
        self.assertEqual(new_token, self.tg.get_token())


if __name__ == '__main__':
    unittest.main()
