"""Fallback tqdm implementation for tests."""

from __future__ import annotations

from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def tqdm(iterable: Iterable[T], **_: object) -> Iterator[T]:
    return iter(iterable)
