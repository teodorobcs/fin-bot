# Import
import logging
import os

# Ensure logs directory exist
logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging settings
logging.basicConfig(
    filename=os.path.join(logs_dir, "netsuite_api.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create logger instance
logger = logging.getLogger(__name__)
