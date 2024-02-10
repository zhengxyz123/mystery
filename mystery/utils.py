from unicodedata import east_asian_width


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


def point_in_polygon(
    polygon: list[tuple[int | float, ...]], point: tuple[int | float, ...]
) -> bool:
    """Use raycasting to determine if a point is inside a polygon

    This function is an example implementation available under MIT License at:
    https://www.algorithms-and-technologies.com/point_in_polygon/python
    """
    odd = False
    i, j = -1, len(polygon) - 1
    while i < len(polygon) - 1:
        i = i + 1
        if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and (
            point[0]
            < (
                (polygon[j][0] - polygon[i][0])
                * (point[1] - polygon[i][1])
                / (polygon[j][1] - polygon[i][1])
            )
            + polygon[i][0]
        ):
            odd = not odd
        j = i
    return odd


__all__ = "line_break_ascii", "line_break_cjk", "point_in_polygon"
