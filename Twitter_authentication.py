from requests_oauthlib import OAuth1Session
from django.conf import settings
from django.db import models


def twitter_auth(self):
    # ask twitter for authorization credentials

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    app_call_back_url = 'https://dataprivacy.herokuapp.com/' #settings.TWITTER_CALL_BACK_URL

    oauth = OAuth1Session(
            'API_KEY', #settings.TWITTER_API_KEY
            client_secret= 'API_SECRET_KEY', #TWITTER_API_SECRET_KEY
            signature_type='auth_header',
            callback_uri=app_call_back_url
    )

    #recieve authorization credentials from twitter

    response = oauth.fetch_request_token(request_token_url)
    self.twitter_temp_auth_token = response.get('oauth_token')
    self.twitter_temp_auth_token_secret = response.get('oauth_token_secret')
    self.save()

    #return the authorize url
    return oauth.authorization_url(authorize_url)


def T_callback(self, oauth_token, oauth_verifier):
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(
        'API_KEY_HERE', # settings.TWITTER_API_KEY,
        client_secret=settings.TWITTER_API_SECRET_KEY,
        resource_owner_key=oauth_token,
        resource_owner_secret=self.twitter_temp_oauth_token_secret,
        verifier=oauth_verifier,
        signature_type='auth_header')
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    ...


def t_user_search(self, content):
    tweet_url = 'https://api.twitter.com/1.1/user/search.json'
    oauth = OAuth1Session(
        'API_KEY', # settings.TWITTER_API_KEY,
        client_secret='API_SECRET_KEY', # settings.TWITTER_API_SECRET_KEY,
        resource_owner_key=self.twitter_oauth_token,
        resource_owner_secret=self.twitter_oauth_token_secret,
        signature_type='auth_header')

    # enter the search criteria
    # return oauth.post(tweet_url, data={'status': content})
