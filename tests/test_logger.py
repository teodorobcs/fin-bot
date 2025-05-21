import os
import json
import importlib
import tempfile
from pathlib import Path

def test_log_interaction_writes_jsonl(tmp_path):
    # 1 Set env var before the module is imported
    log_file = tmp_path / "out.jsonl"
    os.environ["CHATBOT_LOG_PATH"] = str(log_file)

    # 2 Now import (or reload) the logger so it picks up the new path
    from app import logger
    importlib.reload(logger)              # ensure it re-reads CHATBOT_LOG_PATH
    log_interaction = logger.log_interaction

    # 3 Act
    log_interaction(
        user_id="U-demo",
        query="Ping",
        tool=None,
        args=None,
        result=None,
        reply="Pong",
    )

    # 4 Assert
    with Path(log_file).open() as fh:
        line = json.loads(fh.readline())

    assert line["user_id"] == "U-demo"
    assert line["reply"] == "Pong"