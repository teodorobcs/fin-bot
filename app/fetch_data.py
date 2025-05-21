import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from app.logger import logger

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
    """Fetches full data from NetSuite API, including detailed records for list-based endpoints."""
    base_url = f"https://{NETSUITE_ACCOUNT_URL}.suitetalk.api.netsuite.com/services/rest/record/v1/{endpoint}"
    auth = OAuth1(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        TOKEN_ID,
        TOKEN_SECRET,
        signature_method="HMAC-SHA256",
        signature_type="AUTH_HEADER",
        realm=NETSUITE_ACCOUNT
    )

    try:
        response = requests.get(base_url, auth=auth)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Success: Retrieved list from {endpoint}. Status code: {response.status_code}")

        # If only IDs are returned, fetch full records
        if "items" in data and all("id" in item and "links" in item and len(item) <= 2 for item in data["items"]):
            full_items = []
            for item in data["items"]:
                item_id = item["id"]
                detail_url = f"{base_url}/{item_id}"
                detail_resp = requests.get(detail_url, auth=auth)
                if detail_resp.status_code == 200:
                    full_items.append(detail_resp.json())
                else:
                    logger.warning(f"Failed to fetch full record for {endpoint} ID {item_id}. Status: {detail_resp.status_code}. Body: {detail_resp.text}")
            return {"items": full_items}
        else:
            return data

    except requests.exceptions.RequestException as err:
        logger.error(f"Error fetching {endpoint}: {err}")
        return None