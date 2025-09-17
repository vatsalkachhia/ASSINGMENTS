import sys
from datetime import datetime
from typing import Optional


# Minimal 4-level logger: INFO, WARN, ERROR, DEBUG
_LEVELS = {"INFO": 20, "WARN": 30, "ERROR": 40, "DEBUG": 10}
_CURRENT_LEVEL = _LEVELS["DEBUG"]


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def set_level(level: str) -> None:
    global _CURRENT_LEVEL
    key = level.strip().upper()
    _CURRENT_LEVEL = _LEVELS.get(key, _LEVELS["INFO"])


def get_level() -> str:
    for name, value in _LEVELS.items():
        if value == _CURRENT_LEVEL:
            return name
    return "INFO"


class SimpleLogger:
    def __init__(self, name: Optional[str] = None) -> None:
        self._name = name or "root"

    def info(self, message: str) -> None:
        if _CURRENT_LEVEL <= _LEVELS["INFO"]:
            print(f"{_now_str()} INFO {self._name} - {message}")
    def debug(self, message: str) -> None:
        if _CURRENT_LEVEL <= _LEVELS["DEBUG"]:
            print(f"{_now_str()} DEBUG {self._name} - {message}")

    def warn(self, message: str) -> None:
        if _CURRENT_LEVEL <= _LEVELS["WARN"]:
            print(f"{_now_str()} WARN {self._name} - {message}")

    def error(self, message: str) -> None:
        if _CURRENT_LEVEL <= _LEVELS["ERROR"]:
            sys.stderr.write(f"{_now_str()} ERROR {self._name} - {message}\n")
            sys.stderr.flush()


def get_logger(name: Optional[str] = None) -> SimpleLogger:
    return SimpleLogger(name)


