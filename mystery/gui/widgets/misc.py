from enum import Enum, StrEnum


class Color(StrEnum):
    GREEN = "green"
    BLUE = "blue"
    RED = "red"
    GRAY = "gray"


class Icon(Enum):
    FILE = 1
    SEARCH = 2
    CHAT = 3
    PLUS = 4
    MINUS = 5
    LEFT = 6
    RIGHT = 7
    TICK = 8
    CROSS = 9
    UP = 10
    DOWN = 11


__all__ = "Color", "Icon"
