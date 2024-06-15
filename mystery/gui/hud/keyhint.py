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
    "x",
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
        self._key_move_north = Sprite(
            key_image["up"], 38, 112, batch=batch, group=self._hint_group1
        )
        self._key_move_north.scale = 1.5
        self._key_move_west = Sprite(
            key_image["left"], 15, 89, batch=batch, group=self._hint_group1
        )
        self._key_move_west.scale = 1.5
        self._key_move_south = Sprite(
            key_image["down"], 38, 89, batch=batch, group=self._hint_group1
        )
        self._key_move_south.scale = 1.5
        self._key_move_east = Sprite(
            key_image["right"], 61, 89, batch=batch, group=self._hint_group1
        )
        self._key_move_east.scale = 1.5
        self._key_run = Sprite(
            key_image["shift"], 18, 52, batch=batch, group=self._hint_group1
        )
        self._key_run.scale = 2
        self._key_interact = Sprite(
            key_image["space"], 18, 15, batch=batch, group=self._hint_group1
        )
        self._key_interact.scale = 2

        self._hint_move = Label(
            x=100,
            y=112,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )
        self._hint_run = Label(
            x=100,
            y=68,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )
        self._hint_interact = Label(
            x=100,
            y=31,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group1,
        )

        self._key_open = Sprite(
            key_image["x"], 15, 126, batch=batch, group=self._hint_group2
        )
        self._key_open.scale = 2
        self._key_back = Sprite(
            key_image["escape"], 15, 89, batch=batch, group=self._hint_group2
        )
        self._key_back.scale = 2
        self._key_screenshot = Sprite(
            key_image["f5"], 15, 52, batch=batch, group=self._hint_group2
        )
        self._key_screenshot.scale = 2
        self._key_fullscreen = Sprite(
            key_image["f11"], 15, 15, batch=batch, group=self._hint_group2
        )
        self._key_fullscreen.scale = 2

        self._hint_open = Label(
            x=60,
            y=142,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_back = Label(
            x=60,
            y=105,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_screenshot = Label(
            x=60,
            y=68,
            font_name=FONT_NAME,
            font_size=12,
            anchor_x="left",
            anchor_y="center",
            batch=batch,
            group=self._hint_group2,
        )
        self._hint_fullscreen = Label(
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
            self._hint_open.content_width,
            self._hint_back.content_width,
            self._hint_screenshot.content_width,
            self._hint_fullscreen.content_width,
        )
        self._width2 = 60 + max_width

    @property
    def state(self) -> int:
        return self._state

    def switch_hint(self):
        self._shape.width = self._width2
        self._shape.height = 153
        self._hint_group1.visible = False
        self._hint_group2.visible = True
        self._state = 1

    def hide(self):
        self._hint_group2.visible = False
        self._shape_group.visible = False
        self._state = 2

    def reset(self):
        if self._hint_lang != resmgr.language:
            self._hint_lang = resmgr.language
            self._hint_move.text = resmgr.translate("hint.move")
            self._hint_run.text = resmgr.translate("hint.run")
            self._hint_interact.text = resmgr.translate("hint.interact")
            max_width = max(
                self._hint_move.content_width,
                self._hint_run.content_width,
                self._hint_interact.content_width,
            )
            self._width1 = 100 + max_width

            self._hint_open.text = resmgr.translate("hint.open")
            self._hint_back.text = resmgr.translate("hint.back")
            self._hint_screenshot.text = resmgr.translate("hint.screenshot")
            self._hint_fullscreen.text = resmgr.translate("hint.fullscreen")
            max_width = max(
                self._hint_open.content_width,
                self._hint_back.content_width,
                self._hint_screenshot.content_width,
                self._hint_fullscreen.content_width,
            )
            self._width2 = 60 + max_width

        self._shape.width = self._width1
        self._shape.height = 131
        self._shape_group.visible = True
        self._hint_group1.visible = True
        self._hint_group2.visible = False
        self._state = 0


__all__ = ("KeyHint",)
