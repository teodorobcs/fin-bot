import logging
import os
from pathlib import Path

logs_dir = Path(os.getenv("LOGS_DIR", "logs"))
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)


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