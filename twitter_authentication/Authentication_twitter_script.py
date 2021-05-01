import requests
import os
import json
import base64


def main():
    client_key = "API_KEY_TWTR"
    client_secret = "API_SECRET_KEY_TWTR"

    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-*'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    var = auth_resp.json().keys()

    # check the values to make sure they are correct
    if auth_resp.status_code == 200:
        print("Passed connection test 1")
    else:
        print("Did not pass connection test")

    access_token = auth_resp.json()['access_token']
    return access_token


main()
