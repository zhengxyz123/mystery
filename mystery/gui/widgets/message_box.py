from math import ceil, floor
from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label

from mystery import resmgr, utils
from mystery.gui.patch import ThreePatch
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region
from mystery.resource.manager import FONT_NAME

mb_texture = resmgr.loader.image("textures/gui/message_box.png")
mb_images = []
for i in "lmr":
    mb_images.append(mb_texture.get_region(*texture_region[f"mb{i}"]))


class MessageBox(WidgetBase):
    def __init__(
        self,
        window: "mystery.scenes.GameWindow",
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._window = window
        x, y = 10, 10
        width, height = self._window.width - 20, 78 * 2
        super().__init__(x, y, width, height)

        self._text = ""
        self._back_group = Group(order=0, parent=group)
        self._fore_group = Group(order=1, parent=group)
        self._message = ThreePatch(
            self._x,
            self._y,
            self._width,
            self._height,
            *mb_images,
            batch=batch,
            group=self._back_group,
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
        self._message.group = self._back_group
        self._label.group = self._fore_group

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._label.text = utils.line_break_func(self._text, self._label.width)

    def _update_position(self):
        self._message.x = self._x
        self._message.y = self._y
        self._message.width = self._width
        self._message.height = self._height
        self._label.position = (self._x + 20, 78 * 2 - 25, 0)
        self._label.width = self._width - 40

    def draw(self):
        self._message.draw()
        self._label.draw()

    def resize(self):
        self.width, self.height = self._window.width - 20, 78 * 2
        text = utils.line_break_func(self._text, self._label.width)
        self._label.text = text


__all__ = ("MessageBox",)
