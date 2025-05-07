# Import logging and os modules
import logging
import os

# Define the logs directory (../logs relative to this script)
logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

# Ensure the logs directory exists — create it if it doesn't
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Create a logger instance scoped to the current module
logger = logging.getLogger(__name__)

# Set the logger's minimum level to DEBUG — all messages DEBUG and above will be handled
logger.setLevel(logging.DEBUG)


# -------- FILE HANDLER (for logging to file) -------- #

# Create a file handler that writes to logs/netsuite_api.log
file_handler = logging.FileHandler(os.path.join(logs_dir, "netsuite_api.log"))

# Set the file handler to log INFO and above (skips DEBUG)
file_handler.setLevel(logging.INFO)

# Define a formatter that includes timestamps for file logs
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Attach the formatter to the file handler
file_handler.setFormatter(file_formatter)


# -------- CONSOLE HANDLER (for logging to terminal) -------- #

# Create a stream handler that logs to the console (stdout)
console_handler = logging.StreamHandler()

# Set the console handler to log everything from DEBUG up
console_handler.setLevel(logging.DEBUG)

# Define a cleaner, simpler formatter for console output
console_formatter = logging.Formatter("%(levelname)s - %(message)s")

# Attach the formatter to the console handler
console_handler.setFormatter(console_formatter)


# -------- ATTACH HANDLERS TO LOGGER -------- #

# Add both handlers to the logger instance
logger.addHandler(file_handler)
logger.addHandler(console_handler)