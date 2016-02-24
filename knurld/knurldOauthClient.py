import oauth.oauth as oauth
import httplib
import time
import urlparse

# TODO: config it from a secured place
oauth_dict = {'client_id': 'sfgpWaOrgNgLASXQGUQFMdZQA3NmZxG0',
              'client_secret': 'wbjADuCttwnJx0nW'
              }
uri = {'access-token': 'https://api.knurld.io//oauth/client_credential/accesstoken?grant_type=client_credentials', }

BASE_URL = SERVER = 'https://api.knurld.io//'
PORT = 443
REQUEST_TOKEN_URL = 'https://api.knurld.io/oauth/client_credential/accesstoken?grant_type=client_credentials'
ACCESS_TOKEN_URL = 'https://api.knurld.io//oauth/client_credential/accesstoken?grant_type=client_credentials'
AUTHORIZATION_URL = 'https://api.knurld.io/v1/verifications/a67a3f337823e2d56ec264f8c30c9375'
CALLBACK_URL = None
RESOURCE_URL = None
CONSUMER_KEY = oauth_dict['client_id']
CONSUMER_SECRET = oauth_dict['client_secret']


class OAuthClient(oauth.OAuthClient):

    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='',
                 access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection(
                            "%s:%d" % (self.server, self.port))

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    def fetch_access_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method,
                                self.access_token_url, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection.request(oauth_request.http_method, oauth_request.to_url())
        response = self.connection.getresponse()
        return response.read()

    def access_resource(self, oauth_request):
        # via post body
        # -> some protected resources
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.connection.request('POST', RESOURCE_URL,
                                body=oauth_request.to_postdata(),
                                headers=headers)
        response = self.connection.getresponse()
        return response.read()


def pause():
    print('-------------------------------------------------')
    time.sleep(1)


def main():

    # The same following boilerplate can be invoked from the index.py controller

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

    # is there a better way to get the verifier?
    query = urlparse.urlparse(response)[4]
    params = urlparse.parse_qs(query, keep_blank_values=False)
    verifier = params['oauth_verifier'][0]
    print('verifier: %s' % verifier)
    pause()

if __name__ == "__main__":
    main()
    print('Done')
