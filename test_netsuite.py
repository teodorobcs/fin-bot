import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NETSUITE_ACCOUNT = os.getenv("NETSUITE_ACCOUNT")
NETSUITE_CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY")
NETSUITE_CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET")
NETSUITE_TOKEN_ID = os.getenv("NETSUITE_TOKEN_ID")
NETSUITE_TOKEN_SECRET = os.getenv("NETSUITE_TOKEN_SECRET")

# Ensure variables are loaded
if not all([NETSUITE_ACCOUNT, NETSUITE_CONSUMER_KEY, NETSUITE_CONSUMER_SECRET, NETSUITE_TOKEN_ID, NETSUITE_TOKEN_SECRET]):
    raise ValueError("Missing environment variables. Check your .env file.")

# API Endpoint - Testing metadata first before customer data
url = f"https://{NETSUITE_ACCOUNT}.suitetalk.api.netsuite.com/services/rest/metadata-catalog/v1/entity"

# Headers for Token-Based Authentication (TBA)
headers = {
    "Authorization": f"NLAuth nlauth_account={NETSUITE_ACCOUNT}, nlauth_consumerkey={NETSUITE_CONSUMER_KEY}, nlauth_consumersecret={NETSUITE_CONSUMER_SECRET}, nlauth_tokenid={NETSUITE_TOKEN_ID}, nlauth_tokensecret={NETSUITE_TOKEN_SECRET}",
    "Content-Type": "application/json"
}

# Make the request
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes (400, 403, etc.)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    print("Response Text:", response.text)
