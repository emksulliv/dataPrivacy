# this is a python script that authenticates the user with a token and then makes a basic access attempt to
# obtain tweet information

import json
import requests

# url for twitter access
url = "https://api.twitter.com/2/tweets/search/all"

# need to get the bearer token from django config vars
bearer_token = "place_holder"

# just basic parameters for the test authentication
params = {'query': '(from:twitterdev -is:retweet OR #twitterdev', 'tweet.fields': 'author_id'}


def create_header(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def endpoint_connection(url, headers, parameters):
    res = requests.request("GET", url, headers=headers, params=params)
    # check what the response code is
    print(res.status_code)
    if res.status_code != 200:
        raise Exception(res.status_code, res.text)
    return res.json


def main():
    print("in main")
    headers = create_header(bearer_token)
    json_res = endpoint_connection(url, headers, params)
    # print out the JSON received
    print(json.dumps(json_res, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()