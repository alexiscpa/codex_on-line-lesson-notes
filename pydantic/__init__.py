"""Lightweight fallback pydantic stubs for the test environment."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Callable, Optional, TypeVar, get_args, get_origin


class ValidationError(Exception):
    pass


class BaseModel:
    def __init__(self, **data: Any) -> None:
        annotations = getattr(self.__class__, "__annotations__", {})
        for key, value in data.items():
            annotation = annotations.get(key)
            if annotation is not None:
                value = _coerce_value(value, annotation)
            setattr(self, key, value)

    def model_dump(self) -> dict[str, Any]:
        return dict(self.__dict__)


def Field(
    default: Any = None, *, default_factory: Optional[Callable[[], Any]] = None, **_: Any
) -> Any:
    if default_factory is not None:
        return default_factory()
    return default


T = TypeVar("T")


def AfterValidator(_: Callable[[T], T]) -> Callable[[T], T]:
    def decorator(value: T) -> T:
        return value

    return decorator


def _coerce_value(value: Any, annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin in (list, tuple, set, frozenset, Sequence):
        args = get_args(annotation)
        if args:
            item_type = args[0]
            return [ _coerce_value(item, item_type) for item in value ]
    if isinstance(value, dict) and isinstance(annotation, type) and issubclass(
        annotation, BaseModel
    ):
        return annotation(**value)
    return value
