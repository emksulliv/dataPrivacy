import requests
import os

def getAccessToken():
    
    client_id = str(os.environ.get("API_ID_AMZN"))
    client_secret = str(os.environ.get("API_SECRET_KEY_AMZN"))
    base_url = "https://api.amazon.com/auth/o2/token"

    auth_code = ""
    auth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret
        #'code_verifier': '5CFCAiZC0g0OA-jmBmmjTBZiyPCQsnq_2q5k9fD-aAY',
    }

    auth_resp = requests.post(base_url, headers=auth_headers, data=auth_data)