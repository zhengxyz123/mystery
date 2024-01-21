from typing import Dict, Tuple

texture_region: Dict[str, Tuple[int, int, int, int]] = {
    # textures/gui/widgets/buttons.png
    "bnl": (0, 117, 40, 28),
    "bnm": (42, 117, 40, 28),
    "bnr": (84, 117, 40, 28),
    "bhl": (0, 87, 40, 28),
    "bhm": (42, 87, 40, 28),
    "bhr": (84, 87, 40, 28),
    "bpl": (0, 57, 40, 28),
    "bpm": (42, 57, 40, 28),
    "bpr": (84, 57, 40, 28),
    # textures/gui/widgets/frames.png
    "sftl1": (0, 33, 32, 32),
    "sftm1": (33, 33, 32, 32),
    "sftr1": (66, 33, 32, 32),
    "sftl2": (99, 33, 32, 58),
    "sftm2": (132, 33, 32, 58),
    "sftr2": (165, 33, 32, 58),
    "fml": (0, 0, 32, 32),
    "fmm": (33, 0, 32, 32),
    "fmr": (66, 0, 32, 32),
    "fbl": (99, 0, 32, 32),
    "fbm": (132, 0, 32, 32),
    "fbr": (165, 0, 32, 32),
    # textures/gui/widgets/frame_decorations.png
    "fdbnl": (0, 0, 14, 24),
    "fdbnm": (48, 0, 32, 24),
    "fdbnr": (81, 0, 14, 24),
    "fdbpl": (0, 25, 14, 24),
    "fdbpm": (48, 25, 32, 24),
    "fdbpr": (81, 25, 14, 24),
    # textures/gui/widgets/round_buttons_and_icons.png
    "rbn.red": (32, 32, 14, 14),
    "rbh.red": (32, 16, 14, 14),
    "rbp.red": (32, 0, 14, 14),
    "icon.close": (81, 0, 14, 14),
    # textures/gui/message_box.png
    "mbl": (0, 0, 78, 78),
    "mbm": (78, 0, 162, 78),
    "mbr": (240, 0, 78, 78),
}

__all__ = "texture_region"
