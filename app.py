# Use "flask --app app run" To Run

from flask import Flask, jsonify
import os
from dotenv import load_dotenv, dotenv_values 
import requests

app = Flask(__name__)

# Load env file
load_dotenv()

# Aplos global variables
aplos_token_url = os.getenv("APLOS_TOKEN_URL")
aplos_id = os.getenv("APLOS_ID")
aplos_secret = os.getenv("APLOS_SECRET")
aplos_base_url = os.getenv("APLOS_BASE_URL")

# Virtuous global variables
virtuous_token_url = os.getenv("VIRTUOUS_TOKEN_URL")
virtuous_username = os.getenv("VIRTUOUS_USERNAME")
virtuous_password = os.getenv("VIRTUOUS_PASSWORD")


# Gets aplos access token
def get_access_token_aplos():
    # Debug: Print the URL being used
    print(f"DEBUG: Token URL = '{aplos_token_url}'")
    
    # Gets data from .env file
    data = {
        "grant_type": "client_credentials",
        "client_id": aplos_id,
        "client_secret": aplos_secret
    }

    try:
        response = requests.post(aplos_token_url, data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })
        
        # Debug: Print response details
        print(f"DEBUG: Response Status Code = {response.status_code}")
        print(f"DEBUG: Response Headers = {response.headers}")
        print(f"DEBUG: Response Text = '{response.text}'")
        
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Could not connect to {aplos_token_url}")
        print(f"Connection error details: {e}")
        raise

    # Check for non-200 status codes BEFORE trying to parse JSON
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")

    # Check if response has content before parsing
    if not response.text:
        raise Exception(f"Empty response received from Aplos API. Status: {response.status_code}")
    
    try:
        token_info = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response")
        print(f"Response text was: '{response.text}'")
        raise Exception(f"Invalid JSON response from Aplos API: {e}")

    # Return token from json
    return token_info["data"]["token"]

'''
# Gets virtuous access token
def get_access_token_virtuous():

    # Gets data from .env file
    data = {
        "grant_type": "password",
        "username": virtuous_username,
        "password": virtuous_password
    }

    response = requests.post(virtuous_token_url, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    # Checks for codes other than 200 (200 Code: API Accessed Successfully)
    if response.status_code != 200:
        raise Exception(f"Failed to get Virtuous token: {response.status_code} {response.text}")

    token_info = response.json()

    # Return token from json
    return token_info["access_token"]

# Get aplos accounts
def aplos_accounts_get():
    headers = {"Authorization": "Bearer {}".format(get_access_token_aplos())}

    # establish and error check url
    base_url = aplos_base_url
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    if not base_url.endswith("/"):
        base_url += "/"
    url = f"{base_url}accounts"  # Fixed: use base_url instead of aplos_base_url

    # for debugging
    print(f"DEBUG: Authorization header: {headers}")
    print(f"DEBUG: Requesting Aplos URL: {url}")
    
    r = requests.get(url, headers=headers)
    
    print(f"DEBUG: Accounts response status: {r.status_code}")
    print(f"DEBUG: Accounts response text: {r.text}")
    
    response = r.json()
    print("JSON response: {}".format(response))
    return (response)
'''

# Main function
@app.route("/")
def main():
    #Initialize token list
    token_list = []

    # Request access token from aplos
    print("Requesting access token from Aplos...")
    applos_token = get_access_token_aplos()
    print("Access token from Aplos received!\n")
    token_list.append(applos_token)

    # Request access token from virtuous
    print("Requesting access token from Virtuous...")
    # virtuous_token = get_access_token_virtuous()
    # print("Access token from Virtuous received!\n")
    # token_list.append(virtuous_token)

    # aplos_accounts_get()

    return jsonify(token_list)
