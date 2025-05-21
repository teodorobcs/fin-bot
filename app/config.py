import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NETSUITE_ACCOUNT = os.getenv("NETSUITE_ACCOUNT")
NETSUITE_ACCOUNT_URL = os.getenv("NETSUITE_ACCOUNT_URL")
CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET")
TOKEN_ID = os.getenv("NETSUITE_TOKEN_ID")
TOKEN_SECRET = os.getenv("NETSUITE_TOKEN_SECRET")

# Other config settings
MAX_RETRIES = 3
RETRY_DELAY = 2

print(f"Connected to NetSuite Account: {NETSUITE_ACCOUNT}")