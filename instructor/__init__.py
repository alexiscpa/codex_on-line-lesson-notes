"""Fallback instructor stubs for tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class Mode:
    JSON = "json"


@dataclass
class Instructor:
    chat: Any = None


def from_openai(*_: Any, **__: Any) -> Instructor:
    return Instructor()
