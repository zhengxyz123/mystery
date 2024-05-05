from math import dist
from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import mouse

from mystery import resmgr
from mystery.gui.patch import NinePatch
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region
from mystery.resource.manager import FONT_NAME

frame_texture = resmgr.loader.image("textures/gui/widgets/frames.png")
button_and_icon_texture = resmgr.loader.image(
    "textures/gui/widgets/round_buttons_and_icons.png"
)
icon_image = button_and_icon_texture.get_region(*texture_region["icon.close"])
button_image = {}
for status in ["normal", "hover", "pressed"]:
    button_image[status] = button_and_icon_texture.get_region(
        *texture_region[f"rb{status[0]}.red"]
    )
advanced_frame_image = []
for i in "tmb":
    for j in "lmr":
        region = f"sft{j}2" if i == "t" else f"f{i}{j}"
        advanced_frame_image.append(frame_texture.get_region(*texture_region[region]))
simple_frame_image = []
for i in "tmb":
    for j in "lmr":
        region = f"sft{j}1" if i == "t" else f"f{i}{j}"
        simple_frame_image.append(frame_texture.get_region(*texture_region[region]))


class AdvancedFrame(WidgetBase):
    """A frame with a title and a close button."""

    def __init__(
        self,
        title: str,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, width, height)
        self._pressed = False
        self._button_center = (0, 0)
        self._frame_group = Group(order=0, parent=group)
        self._widgets_group = Group(order=1, parent=group)
        self._icon_group = Group(order=2, parent=group)
        self._button_sprite = Sprite(
            button_image["normal"], batch=batch, group=self._widgets_group
        )
        self._button_sprite.scale = 2
        self._icon_sprite = Sprite(icon_image, batch=batch, group=self._icon_group)
        self._icon_sprite.scale = 2
        self._frame = NinePatch(
            self._x,
            self._y,
            self._width,
            self._height,
            *advanced_frame_image,
            batch=batch,
            group=self._frame_group,
        )
        self._frame.scale = 2
        self._label = Label(
            title,
            font_name=FONT_NAME,
            font_size=18,
            anchor_y="top",
            batch=batch,
            group=self._widgets_group,
        )

    def _check_hit(self, x, y):
        return dist(self._button_center, (x, y)) <= 14

    def _update_position(self):
        self._frame.update(x=self._x, y=self._y, width=self._width, height=self._height)
        wc, hc = self._frame[(0, 0)].width, self._frame[(0, 0)].height
        wm, hm = self._frame[(1, 1)].width, self._frame[(1, 1)].height
        self._button_sprite.position = (
            self._x + self._width - wc + 14,
            self._y + self._height - hc + 78,
            0,
        )
        self._icon_sprite.position = self._button_sprite.position
        self._button_center = (self._button_sprite.x + 14, self._button_sprite.y + 14)
        self._label.position = (self._x + 12, self._y + self._height - hc + 96, 0)

    @property
    def aabb(self) -> tuple[int, ...]:
        x, y, _ = self._button_sprite.position
        return x, y, x + 28, y + 28

    @property
    def group(self) -> Group:
        return self._frame_group.parent

    @group.setter
    def group(self, group: Group):
        self._frame_group = Group(order=0, parent=group)
        self._widgets_group = Group(order=1, parent=group)
        self._icon_group = Group(order=2, parent=group)
        self._frame.group = self._frame_group
        self._label.group = self._widgets_group
        self._button_sprite.group = self._widgets_group
        self._icon_sprite.group = self._icon_group

    @property
    def title(self) -> str:
        return self._label.text

    @title.setter
    def title(self, text: str):
        self._label.text = text

    def draw(self):
        self._frame.draw()
        self._label.draw()
        self._button_sprite.draw()
        self._icon_sprite.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._check_hit(x, y) or not buttons & mouse.LEFT:
            return
        self._pressed = True
        self._button_sprite.image = button_image["pressed"]

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self._pressed:
            return
        self._pressed = False
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button_sprite.image = button_image[status]
        self.dispatch_event("on_button_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if self._pressed:
            return
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button_sprite.image = button_image[status]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._pressed:
            return
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button_sprite.image = button_image[status]


AdvancedFrame.register_event_type("on_button_click")


class SimpleFrame(WidgetBase):
    """A useless frame."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, width, height)
        self._frame = NinePatch(
            self._x,
            self._y,
            self._width,
            self._height,
            *simple_frame_image,
            batch=batch,
            group=group,
        )

    def _update_position(self):
        self._frame.update(x=self._x, y=self._y, width=self._width, height=self._height)

    @property
    def group(self) -> Group:
        return self._frame.group

    @group.setter
    def group(self, group: Group):
        self._frame.group = group

    def draw(self):
        self._frame.draw()


__all__ = "SimpleFrame", "AdvancedFrame"
