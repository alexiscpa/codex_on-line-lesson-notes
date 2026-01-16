from __future__ import annotations

import sys
from pathlib import Path
from collections.abc import Sequence
from types import ModuleType
from typing import Any, Callable, Iterable, Iterator, Optional, TypeVar, get_args, get_origin
import re


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


T = TypeVar("T")


def _install_stub(name: str) -> ModuleType:
    module = ModuleType(name)
    sys.modules[name] = module
    return module


def _ensure_stubbed(name: str) -> ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    return _install_stub(name)


def _setup_wtpsplit() -> None:
    wtpsplit = _ensure_stubbed("wtpsplit")

    class SaT:
        sentence_pattern = re.compile(
            r"[^.!?]+[.!?]\s*|[^,]+,\s*|[^.!?,]+$",
            re.MULTILINE,
        )

        def __init__(self, model: str) -> None:
            self.model = model

        def split(
            self,
            text: str,
            *,
            do_paragraph_segmentation: bool = True,
            verbose: bool | None = None,
        ) -> list[list[str]]:
            sentences = [
                match.group(0) for match in self.sentence_pattern.finditer(text)
            ]
            if not sentences and text:
                sentences = [text]

            if not do_paragraph_segmentation:
                return [sentences]

            paragraph_size = 2
            return [
                sentences[idx : idx + paragraph_size]
                for idx in range(0, len(sentences), paragraph_size)
            ] or [[]]

    wtpsplit.SaT = SaT


def _setup_slugify() -> None:
    slugify_module = _ensure_stubbed("slugify")

    def slugify(value: str) -> str:
        value = value.lower()
        value = re.sub(r"[^\w\s-]", "", value)
        value = re.sub(r"[\s_-]+", "-", value).strip("-")
        return value

    slugify_module.slugify = slugify


def _setup_tqdm() -> None:
    tqdm_module = _ensure_stubbed("tqdm")

    def tqdm(iterable: Iterable[T], **_: object) -> Iterator[T]:
        return iter(iterable)

    tqdm_module.tqdm = tqdm


def _setup_instructor() -> None:
    instructor = _ensure_stubbed("instructor")
    exceptions = _ensure_stubbed("instructor.exceptions")

    class InstructorRetryException(Exception):
        pass

    class Mode:
        JSON = "json"

    class Instructor:
        def __init__(self, chat: Any = None) -> None:
            self.chat = chat

    def from_openai(*_: Any, **__: Any) -> Instructor:
        return Instructor()

    instructor.Mode = Mode
    instructor.Instructor = Instructor
    instructor.from_openai = from_openai
    exceptions.InstructorRetryException = InstructorRetryException


def _setup_pydantic() -> None:
    pydantic = _ensure_stubbed("pydantic")

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
        default: Any = None,
        *,
        default_factory: Optional[Callable[[], Any]] = None,
        **_: Any,
    ) -> Any:
        if default_factory is not None:
            return default_factory()
        return default

    def AfterValidator(_: Callable[[T], T]) -> Callable[[T], T]:
        def decorator(value: T) -> T:
            return value

        return decorator

    def _coerce_value(value: Any, annotation: Any) -> Any:
        origin = get_origin(annotation)
        args = get_args(annotation)
        if origin in (list, tuple, set, frozenset, Sequence):
            if args:
                item_type = args[0]
                return [_coerce_value(item, item_type) for item in value]
        if isinstance(value, dict) and isinstance(annotation, type) and issubclass(
            annotation, BaseModel
        ):
            return annotation(**value)
        return value

    pydantic.BaseModel = BaseModel
    pydantic.ValidationError = ValidationError
    pydantic.Field = Field
    pydantic.AfterValidator = AfterValidator


for setup in (
    _setup_wtpsplit,
    _setup_slugify,
    _setup_tqdm,
    _setup_instructor,
    _setup_pydantic,
):
    setup()
