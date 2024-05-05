from typing import Optional

from pyglet import clock
from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import key

from mystery import resmgr
from mystery.resource.manager import FONT_NAME

key_image = {}
for name in [
    "escape",
    "left",
    "right",
    "up",
    "down",
    "shift",
    "space",
    "f5",
    "f11",
    "e",
]:
    key_image[name] = resmgr.loader.image(f"textures/keys/{name}.png")


class KeyHint:
    def __init__(
        self,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._group = Group(order=0, parent=group)
        self._shape_group = Group(order=0, parent=self._group)
        self._hint_group1 = Group(order=1, parent=self._group)
        self._hint_group2 = Group(order=2, parent=self._group)
        self._hint_group2.visible = False
        self._hint_lang = ""
        self._state = 0

        self._shape = Rectangle(
            10,
            10,
            100,
            131,
            color=(89, 86, 82, 192),
            batch=batch,
            group=self._shape_group,
        )
        self._key_up = Sprite(
            key_image["up"], 38, 112, batch=batch, group=self._hint_group1
        )
        self._key_up.scale = 1.5
        self._key_left = Sprite(
            key_image["left"], 15, 89, batch=batch, group=self._hint_group1
        )
        self._key_left.scale = 1.5
        self._key_down = Sprite(
            key_image["down"], 38, 89, batch=batch, group=self._hint_group1
        )
        self._key_down.scale = 1.5
        self._key_right = Sprite(
            key_image["right"], 61, 89, batch=batch, group=self._hint_group1
        )
        self._key_right.scale = 1.5
        self._key_shift = Sprite(
            key_image["shift"], 18, 52, batch=batch, group=self._hint_group1
        )
        self._key_shift.scale = 2
        self._key_space = Sprite(
            key_image["space"], 18, 15, batch=batch, group=self._hint_group1
        )
        self._key_space.scale = 2

        self._hint_arrow = Label(
            x=100,
            y=112,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )
        self._hint_shift = Label(
            x=100,
            y=68,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )
        self._hint_space = Label(
            x=100,
            y=31,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )

        self._key_e = Sprite(
            key_image["e"], 15, 126, batch=batch, group=self._hint_group2
        )
        self._key_e.scale = 2
        self._key_esc = Sprite(
            key_image["escape"], 15, 89, batch=batch, group=self._hint_group2
        )
        self._key_esc.scale = 2
        self._key_f5 = Sprite(
            key_image["f5"], 15, 52, batch=batch, group=self._hint_group2
        )
        self._key_f5.scale = 2
        self._key_f11 = Sprite(
            key_image["f11"], 15, 15, batch=batch, group=self._hint_group2
        )
        self._key_f11.scale = 2

        self._hint_e = Label(
            x=60,
            y=142,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_esc = Label(
            x=60,
            y=105,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_f5 = Label(
            x=60,
            y=68,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_f11 = Label(
            x=60,
            y=31,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        max_width = max(
            self._hint_e.content_width,
            self._hint_esc.content_width,
            self._hint_f5.content_width,
            self._hint_f11.content_width,
        )
        self._width2 = 60 + max_width

    def on_key_press(self, symbol, modifiers):
        if self._state < 0:
            return
        if key.LEFT <= symbol <= key.DOWN and self._state == 0:
            clock.schedule_once(self.update1, 3)
            self._state = 1
        elif symbol == key.E and self._state == 1:
            clock.schedule_once(self.update2, 3)
            self._state = 2

    def update1(self, dt: float):
        self._shape.width = self._width2
        self._shape.height = 153
        self._hint_group1.visible = False
        self._hint_group2.visible = True

    def update2(self, dt: float):
        self._hint_group2.visible = False
        self._shape_group.visible = False

    def reset(self):
        if self._hint_lang != resmgr.language:
            self._hint_lang = resmgr.language
            self._hint_arrow.text = resmgr.translate("hint.arrow")
            self._hint_shift.text = resmgr.translate("hint.shift")
            self._hint_space.text = resmgr.translate("hint.space")
            max_width = max(
                self._hint_arrow.content_width,
                self._hint_shift.content_width,
                self._hint_space.content_width,
            )
            self._width1 = 100 + max_width

            self._hint_e.text = resmgr.translate("hint.e")
            self._hint_esc.text = resmgr.translate("hint.escape")
            self._hint_f5.text = resmgr.translate("hint.f5")
            self._hint_f11.text = resmgr.translate("hint.f11")
            max_width = max(
                self._hint_e.content_width,
                self._hint_esc.content_width,
                self._hint_f5.content_width,
                self._hint_f11.content_width,
            )
            self._width2 = 60 + max_width

        self._shape.width = self._width1
        self._shape.height = 131
        self._shape_group.visible = True
        self._hint_group1.visible = True
        self._hint_group2.visible = False
        self._state = 0


__all__ = ("KeyHint",)
