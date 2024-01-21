from unicodedata import east_asian_width


def line_break_ascii(s: str, width: int, font_width: int = 24) -> str:
    return s


def line_break_cjk(s: str, line_width: int, font_width: int = 24) -> str:
    breaked = ""
    now_width = 0
    for i in range(len(s)):
        if s[i] == "\n":
            breaked += "\n"
            now_width = 0
            continue
        char_width = font_width if east_asian_width(s[i]) in "FW" else 0.5 * font_width
        if now_width + char_width > line_width:
            breaked += " " + s[i]
            now_width = char_width
        else:
            breaked += s[i]
            now_width += char_width
    return breaked


__all__ = "line_break_ascii", "line_break_cjk"
