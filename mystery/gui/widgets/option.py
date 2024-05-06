from typing import Optional

from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle
from pyglet.text import Label
from pyglet.window import mouse

from mystery.gui.widgets import WidgetBase
from mystery.resource.manager import FONT_NAME

WHITE = (255, 255, 255)
GRAY = (170, 170, 170, 255)


class OptionBase(WidgetBase):
    def __init__(self, x: int, y: int, width: int, height: int, value: str):
        super().__init__(x, y, width, height)
        self._value = value
        self._selected = False

    @property
    def value(self) -> str:
        return self._value

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        if value:
            self.dispatch_event("on_option_toggle", self)


OptionBase.register_event_type("on_option_toggle")


class OptionGroup(EventDispatcher):
    """A group to manage several options.

    It isn't the `Group` in pyglet!!
    """

    def __init__(self):
        self._now = 0
        self._options_list = []
        self._value = ""

    @property
    def value(self) -> str:
        return self._value

    def add(self, *options: OptionBase):
        for option in options:
            if option in self._options_list:
                return
            self._options_list.append(option)
            option.set_handler("on_option_toggle", self.on_toggle)

    def on_toggle(self, which: OptionBase):
        assert which in self._options_list
        if self._options_list[self._now] is which:
            return
        self._options_list[self._now].selected = False
        self._now = self._options_list.index(which)
        self._value = self._options_list[self._now].value
        self.dispatch_event("on_change")


OptionGroup.register_event_type("on_change")


class LanguageSelectOption(OptionBase):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        value: str = "",
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, width, height, value or text)
        self._pressed = False
        self._shape_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._shape = Rectangle(
            self._x,
            self._y,
            self._width,
            self._height,
            color=(128, 128, 128, 0),
            batch=batch,
            group=self._shape_group,
        )
        self._label = Label(
            text,
            x=self._x + self._width // 2,
            y=self._y + self._height // 2,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name=FONT_NAME,
            font_size=18,
            batch=batch,
            group=self._label_group,
        )

    @property
    def group(self) -> Group:
        return self._shape_group.parent

    @group.setter
    def group(self, group: Group):
        self._shape_group = Group(order=0, parent=group)
        self._label_group = Group(order=1, parent=group)
        self._shape.group = self._shape_group
        self._label.group = self._label_group

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        if value:
            self._shape.opacity = 128
            self.dispatch_event("on_option_toggle", self)
        else:
            self._shape.opacity = 0
        self._selected = value

    def _update_position(self):
        self._shape.position = (self._x, self._y)
        self._shape.width = self._width
        self._shape.height = self._height
        self._label.position = (
            self._x + self._width // 2,
            self._y + self._height // 2,
            0,
        )

    def draw(self):
        self._shape.draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.enabled or not self._check_hit(x, y) or not buttons & mouse.LEFT:
            return
        self._label.color = GRAY
        self._pressed = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or not self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE
        self._pressed = False
        if not self._selected:
            self.selected = not self._selected

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self._pressed:
            return
        self._label.color = GRAY if self._check_hit(x, y) else WHITE


__all__ = "OptionBase", "OptionGroup"
