from unicodedata import east_asian_width

from mystery.tiled import Object


def line_break_ascii(text: str, line_width: int, font_width: int = 24) -> str:
    return text


def line_break_cjk(text: str, line_width: int, font_width: int = 24) -> str:
    # Automatically wrap paragraph in `text` so that the width of each line
    # does not exceed `line_width`. `font_width` is the width of a full-width
    # CJK character, such as "あ" or "中".
    if text == "":
        return text
    breaked = text[0]
    fw, fwh = font_width, font_width // 2
    now_width = fw if east_asian_width(text[0]) in "FW" else fwh
    punctuation = "。，、；："
    for i in range(1, len(text)):
        prev, this = text[i - 1], text[i]
        cw1 = fw if east_asian_width(prev) in "FW" else fwh
        cw2 = fw if east_asian_width(this) in "FW" else fwh
        if this == "\n":
            breaked += "\n"
            now_width = 0
        elif this in punctuation and now_width + cw2 > line_width:
            breaked = breaked[:-1] + "\n" + prev + this
            now_width = cw1 + cw2
        elif now_width + cw2 > line_width:
            breaked += "\n" + this
            now_width = cw2
        else:
            breaked += this
            now_width += cw2
    return breaked


class Rect:
    """A simple rectangle for collision test."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def __contains__(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        return (
            self._x <= px <= self._x + self._width
            and self._y <= py <= self._y + self._height
        )

    def __repr__(self) -> str:
        return f"Rect(x={self._x}, y={self._y}, w={self._width}, h={self._height})"

    @classmethod
    def from_tmx_obj(cls, obj: Object):
        rect = cls(obj.x, obj.y, obj.width, obj.height)
        return rect


__all__ = "line_break_ascii", "line_break_cjk", "Rect"
