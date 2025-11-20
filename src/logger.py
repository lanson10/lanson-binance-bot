# src/logger.py
from __future__ import annotations
import logging
import logging.handlers
import json
from typing import Any, Dict

LOG_FILE = "bot.log"

def _format_record(record: logging.LogRecord) -> str:
    payload: Dict[str, Any] = {
        "time": record.asctime if hasattr(record, "asctime") else None,
        "level": record.levelname,
        "message": record.getMessage(),
        "module": record.module,
        "funcName": record.funcName,
    }
    return json.dumps(payload, default=str)

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.asctime = self.formatTime(record, self.datefmt)
        return _format_record(record)

def get_logger(name: str = "binance_bot") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(JSONFormatter())

    # File handler (rotating)
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    fh.setLevel(logging.INFO)
    fh.setFormatter(JSONFormatter())

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
