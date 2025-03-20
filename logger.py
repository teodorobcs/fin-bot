# Import
import logging
import os

# Ensure logs directory exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging settings
logging.basicConfig(
    filename="netsuite_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create logger instance
logger = logging.getLogger(__name__)
