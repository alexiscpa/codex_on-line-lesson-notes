"""Fallback implementation of the wtpsplit SaT interface used in tests."""

from __future__ import annotations

import re
import typing


class SaT:
    """Simplified Segment Any Text (SaT) splitter.

    This fallback provides enough behavior for unit and integration tests without
    requiring the external wtpsplit dependency.
    """

    sentence_pattern = re.compile(r"[^.!?]+[.!?]\s*", re.MULTILINE)

    def __init__(self, model: str) -> None:
        self.model = model

    def split(
        self,
        text: str,
        *,
        do_paragraph_segmentation: bool = True,
        verbose: bool | None = None,
    ) -> typing.List[typing.List[str]]:
        sentences = [match.group(0) for match in self.sentence_pattern.finditer(text)]
        if not sentences and text:
            sentences = [text]

        if not do_paragraph_segmentation:
            return [sentences]

        paragraphs: typing.List[typing.List[str]] = []
        paragraph_size = 3
        for idx in range(0, len(sentences), paragraph_size):
            paragraphs.append(sentences[idx : idx + paragraph_size])

        if not paragraphs:
            paragraphs = [[]]

        return paragraphs
