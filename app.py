# .env file format:

"""
# Aplos Keys
APLOS_CLIENT_ID=""
APLOS_PRIVATE_KEY_PATH=""
APLOS_TOKEN_URL=https://app.aplos.com/hermes/api/v1/partners/verify
APLOS_BASE_URL=https://app.aplos.com/hermes/api/v1


# Virtuous Keys
VIRTUOUS_USERNAME=""
VIRTUOUS_PASSWORD=""
VIRTUOUS_TOKEN_URL=https://api.virtuoussoftware.com/Token
"""

# Use "flask --app app run" To Run

from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import requests
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Aplos configuration
aplos_client_id = os.getenv("APLOS_CLIENT_ID")
aplos_private_key = os.getenv("APLOS_PRIVATE_KEY")
aplos_base_url = os.getenv("APLOS_BASE_URL")

# Virtuous configuration
virtuous_token_url = os.getenv("VIRTUOUS_TOKEN_URL")
virtuous_username = os.getenv("VIRTUOUS_USERNAME")
virtuous_password = os.getenv("VIRTUOUS_PASSWORD")

# Debug: Verify variables are loaded
print("=" * 50)
print("ENVIRONMENT VARIABLES CHECK:")
print(f"APLOS_CLIENT_ID: {aplos_client_id}")
print(f"APLOS_PRIVATE_KEY: {aplos_private_key}")
print(f"APLOS_BASE_URL: {aplos_base_url}")
print("=" * 50)


def load_private_key_from_env():
    """Load RSA private key from environment variable"""
    key_data = os.getenv("APLOS_PRIVATE_KEY")
    if not key_data:
        raise Exception("APLOS_PRIVATE_KEY not found in .env")

    try:
        # Convert escaped newlines to actual newlines
        key_data = key_data.replace('\\n', '\n')

        private_key = serialization.load_pem_private_key(
            key_data.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        return private_key
    except Exception as e:
        raise Exception(f"Error loading private key from environment: {e}")


def decrypt_token(encrypted_token_base64, private_key):
    """Decrypt the Aplos token using the private RSA key"""
    try:
        # Decode the base64 encoded token
        encrypted_token = base64.b64decode(encrypted_token_base64)
        
        # Decrypt using RSA private key
        decrypted_token = private_key.decrypt(
            encrypted_token,
            padding.PKCS1v15()  # Aplos uses PKCS1 padding
        )
        
        # Return as string
        return decrypted_token.decode('utf-8')
    except Exception as e:
        raise Exception(f"Error decrypting token: {e}")


def get_access_token_aplos():
    """Get and decrypt Aplos API access token"""
    
    # Validate environment variables
    if not aplos_client_id:
        raise ValueError("APLOS_CLIENT_ID not set in .env file")
    if not aplos_private_key:
        raise ValueError("APLOS_PRIVATE_KEY not set in .env file")
    
    # Step 1: Request encrypted token from Aplos
    auth_url = f"https://app.aplos.com/hermes/api/v1/auth/{aplos_client_id}"
    
    print(f"Requesting encrypted token from: {auth_url}")
    
    try:
        response = requests.get(auth_url)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Extract encrypted token from response
        encrypted_token = token_data["data"]["token"]
        print(f"Received encrypted token (first 50 chars): {encrypted_token[:50]}...")
        
        # Step 2: Load private key
        print("Loading private key...")
        private_key = load_private_key_from_env()
        
        # Step 3: Decrypt the token
        print("Decrypting token...")
        decrypted_token = decrypt_token(encrypted_token, private_key)
        
        print("✓ Token successfully decrypted!")
        return decrypted_token
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to request Aplos token: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected response format: {token_data}. Missing key: {e}")
    except Exception as e:
        raise Exception(f"Aplos authentication error: {e}")


def get_access_token_virtuous():
    """Get Virtuous API access token"""
    
    if not all([virtuous_token_url, virtuous_username, virtuous_password]):
        raise ValueError("Missing Virtuous credentials in .env file")
    
    data = {
        "grant_type": "password",
        "username": virtuous_username,
        "password": virtuous_password
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(virtuous_token_url, data=data, headers=headers)
        response.raise_for_status()
        
        token_info = response.json()
        return token_info["access_token"]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Virtuous API error: {e}")


def aplos_accounts_get(access_token):
    """Get accounts from Aplos using the decrypted token"""
    
    url = f"{aplos_base_url}accounts"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    print(f"Fetching accounts from: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        accounts_data = response.json()
        print(f"✓ Successfully retrieved {accounts_data['meta']['resource_count']} accounts")
        
        return accounts_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch Aplos accounts: {e}")


@app.route("/")
def main():
    """Main endpoint to test API authentication"""
    
    results = {}
    
    # Aplos
    try:
        print("\n" + "="*50)
        print("Accessing Aplos API...")
        print("="*50)
        
        aplos_token = get_access_token_aplos()
        results["aplos"] = {
            "status": "success",
            "token_preview": aplos_token[:20] + "..." if aplos_token else None
        }
        
        # Optional: Test fetching accounts
        accounts = aplos_accounts_get(aplos_token)
        results["aplos"]["sample_account"] = accounts["data"]["accounts"][0] if accounts["data"]["accounts"] else None
        
    except Exception as e:
        results["aplos"] = {
            "status": "error",
            "message": str(e)
        }
        print(f"✗ Aplos error: {e}")
    
    # Test Virtuous API
    try:
        print("\n" + "="*50)
        print("Accessing Virtuous API...")
        print("="*50)
        
        virtuous_token = get_access_token_virtuous()
        results["virtuous"] = {
            "status": "success",
            "token_preview": virtuous_token[:20] + "..." if virtuous_token else None
        }
        print("✓ Virtuous token received!")
        
    except Exception as e:
        results["virtuous"] = {
            "status": "error",
            "message": str(e)
        }
        print(f"✗ Virtuous error: {e}")
    
    print("="*50 + "\n")
    
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
