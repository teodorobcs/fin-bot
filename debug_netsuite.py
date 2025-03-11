import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debugging: Print the loaded environment variables
print("NETSUITE_ACCOUNT:", os.getenv("NETSUITE_ACCOUNT"))
print("NETSUITE_CONSUMER_KEY:", os.getenv("NETSUITE_CONSUMER_KEY"))
print("NETSUITE_CONSUMER_SECRET:", os.getenv("NETSUITE_CONSUMER_SECRET"))
print("NETSUITE_TOKEN_ID:", os.getenv("NETSUITE_TOKEN_ID"))
print("NETSUITE_TOKEN_SECRET:", os.getenv("NETSUITE_TOKEN_SECRET"))

# Ensure all required variables are loaded
if not all([os.getenv("NETSUITE_ACCOUNT"), os.getenv("NETSUITE_CONSUMER_KEY"), os.getenv("NETSUITE_CONSUMER_SECRET"), os.getenv("NETSUITE_TOKEN_ID"), os.getenv("NETSUITE_TOKEN_SECRET")]):
    raise ValueError("❌ ERROR: Missing environment variables. Check your .env file.")

# API Endpoint
NETSUITE_ACCOUNT = os.getenv("NETSUITE_ACCOUNT").lower().replace('_', '-')
url = f"https://{NETSUITE_ACCOUNT}.suitetalk.api.netsuite.com/services/rest/metadata-catalog/v1"

# Authorization Header for Token-Based Authentication
headers = {
    "Authorization": f"NLAuth nlauth_account={NETSUITE_ACCOUNT}, nlauth_consumerkey={os.getenv('NETSUITE_CONSUMER_KEY')}, nlauth_consumersecret={os.getenv('NETSUITE_CONSUMER_SECRET')}, nlauth_tokenid={os.getenv('NETSUITE_TOKEN_ID')}, nlauth_tokensecret={os.getenv('NETSUITE_TOKEN_SECRET')}",
    "Content-Type": "application/json"
}

# Debugging: Print API Request Details
print("\nDEBUG: API Request Details")
print("Request URL:", url)
print("Headers:", headers)

# Send Request
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("✅ Success:", response.json())
except requests.exceptions.RequestException as e:
    print(f"❌ Request Failed: {e}")
    print("Response Text:", response.text)