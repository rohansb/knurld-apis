import unittest


class TestAdmin(unittest.TestCase):

    def test_get_access_token_status(self):

        # check the status of the token with Endpoint: https://api.knurld.io/v1/status
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
