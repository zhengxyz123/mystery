from math import ceil, floor
from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label

from mystery import resource
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region

WHITE = (255, 255, 255, 255)
GRAY = (170, 170, 170, 255)
button_texture = resource.loader.image("textures/gui/widgets/buttons.png")
decorated_button_texture = resource.loader.image(
    "textures/gui/widgets/frame_decorations.png"
)
button_image = {}
decorated_button_image = {}
for status in ["normal", "hover", "pressed"]:
    for where in ["left", "middle", "right"]:
        name = f"{status}_{where}"
        region_name = f"b{status[0]}{where[0]}"
        button_image[name] = button_texture.get_region(*texture_region[region_name])
        if status == "hover":
            continue
        region_name = f"fdb{status[0]}{where[0]}"
        decorated_button_image[name] = decorated_button_texture.get_region(
            *texture_region[region_name]
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
        self._sprites_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._sprites = {}
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                decorated_button_image[f"normal_{where}"],
                batch=batch,
                group=self._sprites_group,
            )
            self._sprites[where].scale = 2
        self._label = Label(
            text,
            x=self._x + self._width // 2,
            y=self._y + 48 // 2,
            color=WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name="Unifont",
            font_size=16,
            batch=batch,
            group=self._label_group,
        )
        self._pressed = False

    def _update_position(self):
        image = decorated_button_image["normal_left"]
        wi, hi = image.width, image.height
        w, h = self.width, self.height
        ws = floor((wi * h) / hi)
        wm = ceil(w - 2 * ws)

        self._sprites["middle"].width = wm
        self._sprites["left"].position = (self._x, self._y, 0)
        self._sprites["middle"].position = (self._x + ws, self._y, 0)
        self._sprites["right"].position = (self._x + ws + wm, self._y, 0)
        self._label.position = (self._x + w // 2, self._y + h // 2, 0)

    @property
    def group(self) -> Group:
        return self._sprites_group.parent

    @group.setter
    def group(self, group: Group):
        self._sprites_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        for sprite in self._sprites.values():
            sprite.group = self._sprites_group
        self._label.group = self._label_group

    @property
    def value(self):
        return self._pressed

    def draw(self):
        for where in ["left", "middle", "right"]:
            self._sprites[where].draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled or not self._check_hit(x, y):
            return
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = decorated_button_image[f"pressed_{where}"]
        self._pressed = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or not self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = decorated_button_image[f"normal_{where}"]
        self._pressed = False
        self.dispatch_event("on_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = decorated_button_image[f"normal_{where}"]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = decorated_button_image[f"normal_{where}"]


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
        self._sprites_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._sprites = {}
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                button_image[f"normal_{where}"],
                batch=batch,
                group=self._sprites_group,
            )
        self._label = Label(
            text,
            x=self._x + self._width // 2,
            y=self._y + self._height // 2,
            color=WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name="Unifont",
            font_size=font_size,
            batch=batch,
            group=self._label_group,
        )
        self._pressed = False

    def _update_position(self):
        image = button_image["normal_left"]
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
        self._label.position = (self._x + w // 2, self._y + h // 2, 0)

    @property
    def group(self) -> Group:
        return self._sprites_group.parent

    @group.setter
    def group(self, group: Group):
        self._sprites_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        for sprite in self._sprites.values():
            sprite.group = self._sprites_group
        self._label.group = self._label_group

    @property
    def value(self):
        return self._pressed

    def draw(self):
        for where in ["left", "middle", "right"]:
            self._sprites[where].draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled or not self._check_hit(x, y):
            return
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = button_image[f"pressed_{where}"]
        self._pressed = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or not self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = button_image[f"{status}_{where}"]
        self._pressed = False
        self.dispatch_event("on_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = button_image[f"{status}_{where}"]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = button_image[f"{status}_{where}"]


TextButton.register_event_type("on_click")


__all__ = "DecoratedButton", "TextButton"
