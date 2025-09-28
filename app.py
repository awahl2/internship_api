# Use "flask --app app run" To Run

from flask import Flask
import os
from dotenv import load_dotenv, dotenv_values 
import requests

app = Flask(__name__)


# Load Variables From .env File
load_dotenv()

# Global Variables
aplos_token_url = os.getenv("APLOS_TOKEN_URL")
aplos_id = os.getenv("APLOS_ID")
aplos_secret = os.getenv("APLOS_SECRET")

# Get An Access Token
def get_access_token():

    # Exchanges ID, Secret for Access Token
    data = {
        "grant_type": "client_credentials",
        "client_id": aplos_id,
        "client_secret": aplos_secret
    }

    response = requests.post(aplos_token_url)

    # Checks for Codes Other Than 200 (200 Code: API Accessed Successfully)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")

    token_info = response.json()
    return token_info["access_token"]

@app.route("/")
def hello_world():
    print("Requesting access token...")
    token = get_access_token()
    print("Access token received!\n")
    return token
