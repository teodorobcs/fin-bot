import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from .logger import logger

# Load environment variables
load_dotenv()

from app.config import (
    NETSUITE_ACCOUNT,
    NETSUITE_ACCOUNT_URL,
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TOKEN_ID,
    TOKEN_SECRET
)

# Function to fetch data from NetSuite API
def fetch_data(endpoint):
    """Fetches data from NetSuite API and logs response status."""

    url = f"https://{NETSUITE_ACCOUNT_URL}.suitetalk.api.netsuite.com/services/rest/record/v1/{endpoint}" # Endpoint URL variable
    auth = OAuth1(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        TOKEN_ID,
        TOKEN_SECRET,
        signature_method="HMAC-SHA256",
        signature_type="AUTH_HEADER",
        realm=NETSUITE_ACCOUNT  # THIS MUST BE HERE!!!
    )

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status() # Raise error for non-200 responses

        logger.info(f"Success: Retrieved {endpoint} data. Status code: {response.status_code}")
        return response.json()

    # Error handling
    except requests.exceptions.RequestException as err:
        logger.error(f"Error: {err} - Endpoint: {endpoint}")
        return None # Return non if an error occurs