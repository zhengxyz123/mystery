from math import dist
from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.text import Label

from mystery import resource
from mystery.gui.widgets import WidgetBase
from mystery.resource import texture_region

frame_texture = resource.loader.image("textures/gui/widgets/frames.png")
button_and_icon_texture = resource.loader.image(
    "textures/gui/widgets/round_buttons_and_icons.png"
)
icon_image = button_and_icon_texture.get_region(*texture_region["icon.close"])
button_image = {}
for status in ["normal", "hover", "pressed"]:
    button_image[status] = button_and_icon_texture.get_region(
        *texture_region[f"rb{status[0]}.red"]
    )
advanced_frame_image = {"top": {}, "middle": {}, "bottom": {}}
for i in ["top", "middle", "bottom"]:
    for j in ["left", "middle", "right"]:
        if i == "top":
            region = f"sft{j[0]}2"
        else:
            region = f"f{i[0]}{j[0]}"
        advanced_frame_image[i][j] = frame_texture.get_region(*texture_region[region])
simple_frame_image = {"top": {}, "middle": {}, "bottom": {}}
for i in ["top", "middle", "bottom"]:
    for j in ["left", "middle", "right"]:
        if i == "top":
            region = f"sft{j[0]}1"
        else:
            region = f"f{i[0]}{j[0]}"
        simple_frame_image[i][j] = frame_texture.get_region(*texture_region[region])


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
        self._frame_sprites = {"top": {}, "middle": {}, "bottom": {}}
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j] = Sprite(
                    advanced_frame_image[i][j], batch=batch, group=self._frame_group
                )
                self._frame_sprites[i][j].scale = 2
        self._label = Label(
            title,
            font_name="Unifont",
            font_size=18,
            anchor_y="top",
            batch=batch,
            group=self._widgets_group,
        )

    def _check_hit(self, x, y):
        return dist(self._button_center, (x, y)) <= 14

    def _update_position(self):
        image_top = self._frame_sprites["top"]["left"].image
        image_other = self._frame_sprites["middle"]["middle"].image
        wt, ht = image_top.width * 2, image_top.height * 2
        wo, ho = image_other.width * 2, image_other.height * 2
        w = self.width - wt * 2
        h = self.height - ht - ho

        self._frame_sprites["top"]["middle"].width = w
        self._frame_sprites["middle"]["left"].height = h
        self._frame_sprites["middle"]["middle"].width = w
        self._frame_sprites["middle"]["middle"].height = h
        self._frame_sprites["middle"]["right"].height = h
        self._frame_sprites["bottom"]["middle"].width = w

        self._frame_sprites["bottom"]["left"].position = (self.x, self.y, 0)
        self._frame_sprites["bottom"]["middle"].position = (self.x + wo, self.y, 0)
        self._frame_sprites["bottom"]["right"].position = (self.x + w + wo, self.y, 0)
        self._frame_sprites["middle"]["left"].position = (self.x, self.y + ho, 0)
        self._frame_sprites["middle"]["middle"].position = (self.x + wo, self.y + ho, 0)
        self._frame_sprites["middle"]["right"].position = (
            self.x + w + wo,
            self.y + ho,
            0,
        )
        self._frame_sprites["top"]["left"].position = (self.x, self.y + h + ho, 0)
        self._frame_sprites["top"]["middle"].position = (
            self.x + wo,
            self.y + h + ho,
            0,
        )
        self._frame_sprites["top"]["right"].position = (
            self.x + w + wo,
            self.y + h + ho,
            0,
        )
        self._button_sprite.position = (self.x + w + wo + 14, self.y + h + ho + 78, 0)
        self._icon_sprite.position = self._button_sprite.position
        self._button_center = (self._button_sprite.x + 14, self._button_sprite.y + 14)
        self._label.position = (self.x + 12, self.y + h + ho + 96, 0)

    @property
    def group(self) -> Group:
        return self._frame_group.parent

    @group.setter
    def group(self, group: Group):
        self._frame_group = Group(order=0, parent=group)
        self._widgets_group = Group(order=1, parent=group)
        self._icon_group = Group(order=2, parent=group)
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j].group = self._frame_group
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
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j].draw()
        self._label.draw()
        self._button_sprite.draw()
        self._icon_sprite.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._check_hit(x, y):
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
        self._frame_sprites = {"top": {}, "middle": {}, "bottom": {}}
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j] = Sprite(
                    simple_frame_image[i][j], batch=batch, group=group
                )
                self._frame_sprites[i][j].scale = 2

    def _update_position(self):
        image = self._frame_sprites["top"]["left"].image
        dw, dh = image.width, image.height
        w = self.width - dw * 2
        h = self.height - dh * 2

        self._frame_sprites["top"]["middle"].width = w
        self._frame_sprites["middle"]["left"].height = h
        self._frame_sprites["middle"]["middle"].width = w
        self._frame_sprites["middle"]["middle"].height = h
        self._frame_sprites["middle"]["right"].height = h
        self._frame_sprites["bottom"]["middle"].width = w

        self._frame_sprites["bottom"]["left"].position = (self.x, self.y, 0)
        self._frame_sprites["bottom"]["middle"].position = (self.x + dw, self.y, 0)
        self._frame_sprites["bottom"]["right"].position = (self.x + dw + w, self.y, 0)
        self._frame_sprites["middle"]["left"].position = (self.x, self.y + dh, 0)
        self._frame_sprites["middle"]["middle"].position = (self.x + dw, self.y + dh, 0)
        self._frame_sprites["middle"]["right"].position = (
            self.x + w + dw,
            self.y + dh,
            0,
        )
        self._frame_sprites["top"]["left"].position = (self.x, self.y + h + dh, 0)
        self._frame_sprites["top"]["middle"].position = (
            self.x + dw,
            self.y + h + dh,
            0,
        )
        self._frame_sprites["top"]["right"].position = (
            self.x + w + dw,
            self.y + h + dh,
            0,
        )

    @property
    def group(self) -> Group:
        return self._frame_sprites["top"]["left"].group

    @group.setter
    def group(self, group: Group):
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j].group = group

    def draw(self):
        for i in ["top", "middle", "bottom"]:
            for j in ["left", "middle", "right"]:
                self._frame_sprites[i][j].draw()


__all__ = "SimpleFrame", "AdvancedFrame"
