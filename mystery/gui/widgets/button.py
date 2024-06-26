from math import ceil, floor
from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import mouse

from mystery import resmgr
from mystery.gui.patch import ThreePatch
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region
from mystery.resource.manager import FONT_NAME

WHITE = (255, 255, 255, 255)
GRAY = (170, 170, 170, 255)
button_texture = resmgr.loader.image("textures/gui/widgets/buttons.png")
decorated_button_texture = resmgr.loader.image(
    "textures/gui/widgets/frame_decorations.png"
)
button_image = {"normal": [], "hover": [], "pressed": []}
decorated_button_image = {"normal": [], "pressed": []}
for i in ["normal", "hover", "pressed"]:
    for j in "lmr":
        region_name = f"b{i[0]}{j}"
        button_image[i].append(button_texture.get_region(*texture_region[region_name]))
        if i == "hover":
            continue
        region_name = f"fdb{i[0]}{j}"
        decorated_button_image[i].append(
            decorated_button_texture.get_region(*texture_region[region_name])
        )


class DecoratedButton(WidgetBase):
    """A button placed at the edge of frames."""

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, width, 48)
        self._button_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._button = ThreePatch(
            self._x,
            self._y,
            self._width,
            self._height,
            *decorated_button_image["normal"],
            batch=batch,
            group=self._button_group,
        )
        self._label = Label(
            text,
            x=self._x + self._width // 2,
            y=self._y + 48 // 2,
            color=WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name=FONT_NAME,
            font_size=16,
            batch=batch,
            group=self._label_group,
        )
        self._pressed = False

    @property
    def group(self) -> Group:
        return self._button_group.parent

    @group.setter
    def group(self, group: Group):
        self._button_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._button.group = self._button_group
        self._label.group = self._label_group

    @property
    def text(self) -> str:
        return self._label.text

    @text.setter
    def text(self, text: str):
        self._label.text = text

    @property
    def value(self):
        return self._pressed

    def _update_position(self):
        self._button.update(
            x=self._x, y=self._y, width=self._width, height=self._height
        )
        self._label.position = (
            self._x + self._width // 2,
            self._y + self._height // 2,
            0,
        )

    def draw(self):
        self._button.draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._enabled or not self._check_hit(x, y) or not buttons & mouse.LEFT:
            return
        self._button[:] = decorated_button_image["pressed"]
        self._pressed = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self._enabled or not self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        self._button[:] = decorated_button_image["normal"]
        self._pressed = False
        self.dispatch_event("on_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        self._button[:] = decorated_button_image["normal"]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self._enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        self._button[:] = decorated_button_image["normal"]


DecoratedButton.register_event_type("on_click")


class TextButton(WidgetBase):
    """A button with a line of text."""

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        font_size: int = 24,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, width, height)
        self._button_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._button = ThreePatch(
            self._x,
            self._y,
            self._width,
            self._height,
            *button_image["normal"],
            batch=batch,
            group=self._button_group,
        )
        self._label = Label(
            text,
            x=self._x + self._width // 2,
            y=self._y + self._height // 2,
            color=WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name=FONT_NAME,
            font_size=font_size,
            batch=batch,
            group=self._label_group,
        )
        self._pressed = False

    @property
    def group(self) -> Group:
        return self._button_group.parent

    @group.setter
    def group(self, group: Group):
        self._button_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._button.group = self._button_group
        self._label.group = self._label_group

    @property
    def text(self) -> str:
        return self._label.text

    @text.setter
    def text(self, text: str):
        self._label.text = text

    @property
    def value(self):
        return self._pressed

    def _set_enabled(self, enabled: bool):
        if enabled:
            self._button[:] = button_image["normal"]
            self._label.color = WHITE
        else:
            self._button[:] = button_image["pressed"]
            self._label.color = GRAY

    def _update_position(self):
        self._button.update(
            x=self._x, y=self._y, width=self._width, height=self._height
        )
        self._label.position = (
            self._x + self._width // 2,
            self._y + self._height // 2,
            0,
        )

    def draw(self):
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._enabled or not self._check_hit(x, y) or not buttons & mouse.LEFT:
            return
        self._button[:] = button_image["pressed"]
        self._pressed = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self._enabled or not self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button[:] = button_image[status]
        self._pressed = False
        self.dispatch_event("on_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button[:] = button_image[status]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self._enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        self._button[:] = button_image[status]


TextButton.register_event_type("on_click")


__all__ = "DecoratedButton", "TextButton"
