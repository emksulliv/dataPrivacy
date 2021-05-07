from django.shortcuts import render
import base64
import requests
import os


def button(request):
    return render(request, 'index.html', {})


def search_script(request):
    client_key = str(os.environ.get("API_KEY_TWTR"))
    client_secret = str(os.environ.get("API_SECRET_KEY_TWTR"))

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

    access_token = auth_resp.json()['access_token']

    search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    # val = input("enter search parameters: ")
    search_params = {
        'q': 'NASA',
        'result_type': 'recent',
        'count': 1
    }
    fields = "created_at,description,pinned_tweet_id"
    search_params2 = {"usernames": "Andrew", "user.fields": fields}

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    tweet_data = search_resp.json()

    if tweet_data['statuses'] == "":
        print("Search came up empty")

    # else:
    # print("search test passed")
    # print("printing search results...")
    # print(tweet_data)
    # for x in tweet_data['statuses']:
    # print(x['text'] + '\n')
    # y = x['text']
    # print(x['user'])
    # print(x['coordinates'])

    return render(request, 'index.html', {'data': tweet_data})
