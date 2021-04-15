import requests
import os
import json
import base64

client_key = "place holder"
client_secret = "place_holder"

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
    print("Past connection test 1")
else:
    print("Did not pass connection test")

access_token = auth_resp.json()['access_token']

search_headers = {'Authorization': 'Bearer {}'.format(access_token)}

search_params = {
    'q': 'General Election',
    'result_type': 'recent',
    'count': 2
}

search_url = '{}1.1/search/tweets.json'.format(base_url)

search_resp = requests.get(search_url, headers=search_headers, params=search_params)

# check connection second time
if search_resp.status_code == 200:
    print("Passed connection test 2")
else:
    print("Did not pass connection test 2")

tweet_data = search_resp.json()

for x in tweet_data['statuses']:
    print(x['text'] + '\n')
