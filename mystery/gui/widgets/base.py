from pyglet.gui import WidgetBase as PygletWidgetBase


class WidgetBase(PygletWidgetBase):
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self._update_position()
        self.dispatch_event("on_reposition", self)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self._update_position()
        self.dispatch_event("on_reposition", self)

    @property
    def position(self) -> tuple[int, int]:
        return self._x, self._y

    @position.setter
    def position(self, values: tuple[int, int]):
        self._x, self._y = values
        self._update_position()
        self.dispatch_event("on_reposition", self)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self._update_position()
        self.dispatch_event("on_reposition", self)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self._update_position()
        self.dispatch_event("on_reposition", self)


WidgetBase.register_event_type("on_reposition")


__all__ = ("WidgetBase",)
