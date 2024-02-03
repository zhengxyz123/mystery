from math import ceil, floor
from typing import Optional

from pyglet import clock
from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import Window

from mystery import resmgr, utils
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region
from mystery.resource.manager import FONT_NAME

mb_texture = resmgr.loader.image("textures/gui/message_box.png")
mb_images = {}
for where in ["left", "middle", "right"]:
    name = f"mb{where[0]}"
    mb_images[where] = mb_texture.get_region(*texture_region[name])


class MessageBox(WidgetBase):
    def __init__(
        self,
        window: Window,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._window = window
        x, y = 10, 10
        width, height = self._window.width - 20, 78 * 2
        super().__init__(x, y, width, height)

        self._text = ""
        self._displayed_text = ""
        self._back_group = Group(order=0, parent=group)
        self._fore_group = Group(order=1, parent=group)
        self._sprites = {}
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                mb_images[where], batch=batch, group=self._back_group
            )
        self._label = Label(
            font_name=FONT_NAME,
            font_size=18,
            width=self._width - 40,
            multiline=True,
            batch=batch,
            group=self._fore_group,
        )
        self._update_position()

    @property
    def group(self) -> Group:
        return self._back_group.parent

    @group.setter
    def group(self, group: Group):
        self._back_group = Group(order=0, parent=group)
        self._fore_group = Group(order=1, parent=group)
        for sprite in self._sprites.values():
            sprite.group = self._back_group
        self._label.group = self._fore_group

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._label.text = self._line_break_func(self._text, self._label.width)

    def _line_break_func(self, s: str, width: int) -> str:
        func = getattr(utils, f"line_break_{resmgr.info('line_break_func')}")
        return func(s, width)

    def _update_position(self):
        image = self._sprites["left"].image
        wi, hi = image.width, image.height
        w, h = self.width, self.height
        ws = floor((wi * h) / hi)
        wm = ceil(w - 2 * ws)

        self._sprites["left"].width = ws
        self._sprites["left"].height = h
        self._sprites["middle"].width = wm
        self._sprites["middle"].height = h
        self._sprites["right"].width = ws
        self._sprites["right"].height = h

        self._sprites["left"].position = (self._x, self._y, 0)
        self._sprites["middle"].position = (self._x + ws, self._y, 0)
        self._sprites["right"].position = (self._x + ws + wm, self._y, 0)
        self._label.position = (self._x + 20, 78 * 2 - 25, 0)
        self._label.width = w - 40

    def draw(self):
        for where in ["left", "middle", "right"]:
            self._sprites[where].draw()
        self._label.draw()

    def resize(self):
        self.width, self.height = self._window.width - 20, 78 * 2
        text = self._line_break_func(self._displayed_text, self._label.width)
        self._label.text = text


__all__ = "MessageBox"
