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


# -------- CHATBOT INTERACTION AUDIT LOGGER -------- #
#
# This lightweight helper writes each chatbot turn as a single JSON
# object on its own line.  Use `tail -f` or `jq -c` to inspect, or ship
# to Postgres/ClickHouse later.
#
# Fields:
#   ts      – ISO‑8601 UTC timestamp
#   user_id – caller id the API route passes in
#   query   – raw user prompt
#   tool    – tool name OpenAI decided to call (or None / "error")
#   args    – arguments passed to the tool
#   result  – raw tool result (truncated in UI, full in log)
#   reply   – final assistant message returned to the caller
#
# --------------------------------------------------------------------

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# Chat log path defaults to logs/chatbot_interactions.jsonl at repo root.
CHAT_LOG_PATH = Path(
    os.getenv("CHATBOT_LOG_PATH", os.path.join(logs_dir, "chatbot_interactions.jsonl"))
)
CHAT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def _utc_now_iso() -> str:
    """Return current UTC time in ISO‑8601 with milliseconds."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

def log_interaction(
    *,
    user_id: str,
    query: str,
    tool: str | None,
    args: Dict[str, Any] | None,
    result: Any | None,
    reply: str,
) -> None:
    """Append one chatbot interaction to the JSONL audit file."""
    entry = {
        "ts": _utc_now_iso(),
        "user_id": user_id,
        "query": query,
        "tool": tool,
        "args": args,
        "result": result,
        "reply": reply,
    }
    with CHAT_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")