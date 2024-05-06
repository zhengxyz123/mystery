from __future__ import annotations

from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.gui.widgets import WidgetBase as PygletWidgetBase
from pyglet.shapes import Rectangle, ShapeBase
from pyglet.sprite import Sprite
from pyglet.window import mouse

from mystery.gui.groups import ScissorGroup
from mystery.gui.widgets import WidgetBase


class ScrollableLayout(WidgetBase):
    """A container can be scrolled.

    ScrollableLayout only support vertical scrolling.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        content_height: Optional[int] = None,
        group: Optional[Group] = None,
    ):
        """Create a ScrollableLayout."""
        super().__init__(x, y, width, height)
        self._content_height = content_height or height
        if self._content_height < self._height:
            self._content_height = self._height
        self._offset_y = 0
        self._value = 0
        self._group = ScissorGroup(x, y, width, height, parent=group)
        self._hscroll: Optional[ScrollBar] = None
        self._elements: list[PygletWidgetBase | ShapeBase | Sprite] = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if self._content_height < self._height:
            self._content_height = self._height
        if self._content_height > self._height:
            self._hscroll.visiable = True
        else:
            self.offset_y = 0
            self._hscroll.visiable = False
        self._update_position()

    @property
    def content_height(self) -> int:
        return self._content_height

    @content_height.setter
    def content_height(self, value: int):
        if value < self._height:
            value = self._height
        self._content_height = value
        if self._content_height > self._height:
            self._hscroll.visiable = True
        else:
            self.offset_y = 0
            self._hscroll.visiable = False

    @property
    def hscroll(self):
        return self._hscroll

    @hscroll.setter
    def hscroll(self, scroll_bar: ScrollBar):
        self._hscroll = scroll_bar

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value: int):
        value = max(0, min(self._content_height - self._height, value))
        self.scroll(0, value - self._offset_y)
        self._offset_y = value
        if self._offset_y == 0:
            self._hscroll.value = 0
        else:
            self._hscroll.value = self._offset_y / (self._content_height - self._height)

    def _update_position(self):
        self._group.area = self._x, self._y, self._width, self._height

    def add(self, *elements: PygletWidgetBase | ShapeBase | Sprite):
        """Add some elements to ScrollableLayout.

        Objects that are instanced in `pyglet.gui.widget.WidgetBase`,
        `pyglet.shapes.ShapeBase` and `pyglet.sprite.Sprite` are
        recommended.

        Otherwise, the objects need to have `x`, `y` attributes and
        cannot be `ScrollableLayout` or `ScrollBar`.
        """
        for widget in elements:
            if widget not in self._elements:
                assert hasattr(widget, "x") and hasattr(
                    widget, "y"
                ), "must have x, y attributes"
                if isinstance(widget, (ScrollableLayout, ScrollBar)):
                    raise TypeError(
                        f"{widget.__class__.__name__} cannot add to ScrollableLayout"
                    )
                widget.group = self._group
                self._elements.append(widget)

    def draw(self):
        for widget in self._elements:
            widget.draw()

    def get_point(self, x: int, y: int) -> tuple[int, int]:
        """Get the absolute position of `(x, y)` after the ScrollableLayout
        has been scrolled.

        Returns `(x, y)` itself when it is outside the widget.
        """
        if not self._check_hit(x, y):
            return (x, y)
        return (x, y + self._offset_y)

    def scroll(self, dx: int, dy: int):
        """Scroll the elements added to the ScrollableLayout."""
        for obj in self._elements:
            obj.y += dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self._elements:
            if hasattr(widget, "on_mouse_drag"):
                widget.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self._elements:
            if hasattr(widget, "on_mouse_motion"):
                widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._check_hit(x, y):
            return
        for widget in self._elements:
            if hasattr(widget, "on_mouse_press"):
                widget.on_mouse_press(x, y, buttons, modifiers)

    def on_mouse_release(self, x, y, buttons, modifiers):
        for widget in self._elements:
            if hasattr(widget, "on_mouse_release"):
                widget.on_mouse_release(x, y, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self._hscroll.visiable and self._check_hit(x, y):
            self.offset_y -= 8 * scroll_y

    def on_scrollbar_scroll(self, vx, vy):
        """An event triggered by ScrollBar scrolling."""
        self.offset_y = vy * (self._content_height - self._height)


ScrollableLayout.register_event_type("on_scrollbar_scroll")


class ScrollBar(WidgetBase):
    """A vertical scrollbar."""

    bar_color = {
        "base": (105, 106, 106),
        "normal": (210, 125, 44, 143, 86, 59),
        "pressed": (143, 86, 59, 102, 57, 49),
    }

    def __init__(
        self,
        x: int,
        y: int,
        height: int,
        scrollable_layout: ScrollableLayout,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        super().__init__(x, y, 12, height)
        self._pressd = False
        self._value = 0
        self._visiable = True
        self._scrollable_layout = scrollable_layout
        self._scrollable_layout.hscroll = self
        self._group = Group(order=1024, parent=group)
        self._group0 = Group(order=0, parent=self._group)
        self._group1 = Group(order=1, parent=self._group)
        self._group2 = Group(order=2, parent=self._group)
        self._scrolling_area = Rectangle(
            self._x,
            self._y,
            self._width,
            self._height,
            color=self.bar_color["base"],
            batch=batch,
            group=self._group0,
        )
        self._bbar = Rectangle(
            self._x,
            self._y + self._height - self._height * 0.5,
            self._width,
            self._height * 0.5,
            color=self.bar_color["normal"][3:],
            batch=batch,
            group=self._group1,
        )
        self._fbar = Rectangle(
            self._x,
            self._y + self._height - self._height * 0.5 + 3,
            self._width - 3,
            self._height * 0.5 - 3,
            color=self.bar_color["normal"][:3],
            batch=batch,
            group=self._group2,
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value
        self._update_position()

    @property
    def visiable(self):
        return self._visiable

    @visiable.setter
    def visiable(self, value: bool):
        self._visiable = bool(value)
        self._group.visible = self._visiable
        if not self._visiable:
            self.value = 0
        else:
            self._update_position()

    def _refresh_value(self):
        self._value = (self._y + self._height - self._bbar.y - self._bbar.height) / (
            self._height - self._bbar.height
        )
        self._value = max(0, min(1, self._value))

    def _update_position(self):
        self._scrolling_area.position = (self._x, self._y)
        self._scrolling_area.height = self._height

        self._bbar.height = (
            self._height
            * self._scrollable_layout.height
            / self._scrollable_layout.content_height
        )
        self._fbar.height = self._bbar.height - 3

        self._bbar.position = (
            self._x,
            self._y
            + self._height
            - self._bbar.height
            - self._value * (self._height - self._bbar.height),
        )
        self._fbar.position = (self._x, self._bbar.y + 3)

    def draw(self):
        self._scrolling_area.draw()
        self._bbar.draw()
        self._fbar.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if (
            self._visiable
            and self._check_hit(x, y)
            and (x, y) in self._bbar
            and buttons & mouse.LEFT
        ):
            self._pressd = True
            self._bbar.color = self.bar_color["pressed"][3:]
            self._fbar.color = self.bar_color["pressed"][:3]

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._pressd:
            self._pressd = False
            self._bbar.color = self.bar_color["normal"][3:]
            self._fbar.color = self.bar_color["normal"][:3]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._pressd:
            self._bbar.y = max(
                self._y,
                min(self._y + self._height - self._bbar.height, self._bbar.y + dy),
            )
            self._fbar.y = self._bbar.y + 3
            self._refresh_value()
            self._scrollable_layout.dispatch_event(
                "on_scrollbar_scroll", 0, self._value
            )


__all__ = "ScrollableLayout", "ScrollBar"
