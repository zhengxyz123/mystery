from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import mouse

from mystery import resmgr
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region


class ScrollBar(WidgetBase):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        assert width in [40, 48]
        super().__init__(self, x, y, width, height)


__all__ = ("ScrollBar",)
