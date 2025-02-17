import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables in Python
NETSUITE_ACCOUNT = os.getenv("NETSUITE_ACCOUNT")
NETSUITE_CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY")
NETSUITE_CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET")

print(f"Connected to NetSuite Account: {NETSUITE_ACCOUNT}")