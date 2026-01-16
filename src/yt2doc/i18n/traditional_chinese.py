from opencc import OpenCC

_CONVERTER = OpenCC("s2t")


def to_traditional_chinese(text: str, language_code: str) -> str:
    if language_code != "zh":
        return text
    return _CONVERTER.convert(text)
