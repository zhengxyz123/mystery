from textwrap import wrap
from unicodedata import east_asian_width

from mystery import resmgr


def line_break_en(text: str, line_width: int, font_width: int = 24) -> str:
    if text == "":
        return ""
    breaked = wrap(text, (line_width - 1) // font_width * 2)
    return "\n".join(breaked)


def line_break_cjk(text: str, line_width: int, font_width: int = 24) -> str:
    if text == "":
        return ""
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


def line_break_func(text: str, line_width: int, font_width: int = 24) -> str:
    lang2func = {
        "en": line_break_en,
        "cjk": line_break_cjk,
    }
    if (func := resmgr.translate("language.line_break_func")) in lang2func:
        return lang2func[func](text, line_width, font_width)
    else:
        return line_break_en(text, line_width, font_width)


class Rect:
    """A simple rectangle for collision test."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._walkable = False

    def __contains__(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        return (
            self._x <= px <= self._x + self._width
            and self._y <= py <= self._y + self._height
        )

    def __repr__(self) -> str:
        return f"Rect(x={self._x}, y={self._y}, w={self._width}, h={self._height})"

    @classmethod
    def from_tmx_obj(cls, obj, walkable: bool):
        rect = cls(obj.x, obj.y, obj.width, obj.height)
        rect.walkable = walkable
        return rect

    @property
    def area(self) -> tuple[int, ...]:
        return self._x, self._y, self._width, self._height

    @area.setter
    def area(self, area: tuple[int, ...]):
        self._x, self._y, self._width, self._height = area

    @property
    def walkable(self) -> bool:
        return self._walkable

    @walkable.setter
    def walkable(self, value: bool):
        self._walkable = value


__all__ = "line_break_ascii", "line_break_cjk", "line_break_func", "Rect"
