import json
import base64
import os
import requests
import Authentication_twitter_script


def test():
    base_url = 'https://api.twitter.com/'
    access_token = Authentication_twitter_script.main()

    search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    val = input("enter search parameters: ")
    search_params = {
        'q': val,
        'result_type': 'recent',
        'count': 1
    }
    fields = "created_at,description,pinned_tweet_id"
    search_params2 = {"usernames": "Andrew", "user.fields": fields}

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    # search_url = '{}1.1/users/search.json'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    # check connection second time
    if search_resp.status_code == 200:
        print("Passed connection test 2" + '\n')
    else:
        print("Did not pass connection test 2")

    tweet_data = search_resp.json()

    if tweet_data['statuses'] == "":
        print("Search came up empty")

    else:
        print("search test passed")
        print("printing search results...")
        for x in tweet_data['statuses']:
            print(x['text'] + '\n')
            print(x['user'])
            print(x['coordinates'])


test()
