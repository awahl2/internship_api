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

# Virtuous global variables
virtuous_token_url = os.getenv("VIRTUOUS_TOKEN_URL")
virtuous_username = os.getenv("VIRTUOUS_USERNAME")
virtuous_password = os.getenv("VIRTUOUS_PASSWORD")


# Gets access token
def get_access_token_aplos():

    # Gets data from .env file
    data = {
        "grant_type": "client_credentials",
        "client_id": aplos_id,
        "client_secret": aplos_secret
    }

    response = requests.post(aplos_token_url, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    # Checks for codes other than 200 (200 Code: API Accessed Successfully)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")

    token_info = response.json()

    # Return token from json
    return token_info["data"]["token"]

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
    virtuous_token = get_access_token_virtuous()
    print("Access token from Virtuous received!\n")
    token_list.append(virtuous_token)

    return jsonify(token_list)
