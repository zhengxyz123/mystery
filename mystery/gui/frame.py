from mystery.gui.widgets import WidgetBase


class WidgetFrame:
    """The Frame object, rewritten from `pyglet.gui.frame.Frame`."""

    def __init__(self, window: "mystery.scenes.GameWindow", cell_size=128):
        self._window = window
        self._cell_size = cell_size
        self._cells: dict[tuple[int, int], set[WidgetBase]] = {}
        self._active_widgets: set[WidgetBase] = set()
        self._order = 0
        self._enable = False
        self._mouse_pos = 0, 0

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, status: bool):
        self._enable = bool(status)
        if self._enable:
            self._window.push_handlers(self)
        else:
            self._window.remove_handlers(self)

    def _hash(self, x: int, y: int) -> tuple[int, int]:
        return int(x / self._cell_size), int(y / self._cell_size)

    def _on_reposition_handler(self, widget: WidgetBase):
        self.remove_widget(widget)
        self.add_widget(widget)

    def add_widget(self, *widgets: WidgetBase):
        for widget in widgets:
            min_vec, max_vec = self._hash(*widget.aabb[0:2]), self._hash(
                *widget.aabb[2:4]
            )
            for i in range(min_vec[0], max_vec[0] + 1):
                for j in range(min_vec[1], max_vec[1] + 1):
                    self._cells.setdefault((i, j), set()).add(widget)
            widget.update_groups(self._order)
            widget.set_handler("on_reposition", self._on_reposition_handler)

    def remove_widget(self, *widgets: WidgetBase):
        for widget in widgets:
            for all_widgets in self._cells.values():
                if widget in all_widgets:
                    all_widgets.remove(widget)
                    widget.set_handler("on_reposition", lambda w: None)

    def on_mouse_press(self, x, y, buttons, modifiers):
        for widget in self._cells.get(self._hash(x, y), set()):
            widget.on_mouse_press(x, y, buttons, modifiers)
            self._active_widgets.add(widget)

    def on_mouse_release(self, x, y, buttons, modifiers):
        for widget in self._active_widgets:
            widget.on_mouse_release(x, y, buttons, modifiers)
        self._active_widgets.clear()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self._active_widgets:
            widget.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self._mouse_pos = x, y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for widget in self._cells.get(self._hash(x, y), set()):
            widget.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_motion(self, x, y, dx, dy):
        for cell in self._cells.values():
            for widget in cell:
                widget.on_mouse_motion(x, y, dx, dy)
        self._mouse_pos = x, y

    def on_text(self, text):
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text(text)

    def on_text_motion(self, motion):
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text_motion_select(motion)


__all__ = ("WidgetFrame",)
