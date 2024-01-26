from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.text import Label
from pyglet.window import Window, key, mouse

from mystery import utils
from mystery.gui.widgets import MessageBox
from mystery.scenes import Scene


class StartScene(Scene):
    def __init__(self, window: Window):
        super().__init__(window)
        self.batch = Batch()
        self.mb_group = Group(order=0)
        self.label_group = Group(order=1)
        self.label_group.visible = False
        self.display_on_mb = True
        self.now_plot = 0
        self.plot = []
        self.label_text = ""
        self._load_plots()

        self.message = MessageBox(self.window, self.batch, self.mb_group)
        self.label = Label(
            font_name="Unifont",
            font_size=24,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=0.8 * self.window.width,
            batch=self.batch,
            group=self.label_group,
        )
        self.frame.add_widget(self.message)

    def _line_break_func(self, s: str, width: int) -> str:
        func = getattr(
            utils, f"line_break_{self.window.resource.info('line_break_func')}"
        )
        return func(s, width, 32)

    def _load_plots(self):
        i = 0
        while len(plot := self.window.resource.translate(f"start.plot.{i}")) != 0:
            self.plot.append(plot)
            i += 1

    def _next_plot(self):
        if self.now_plot + 1 >= len(self.plot):
            self.window.switch_scene("menu")
        if self.now_plot + 1 < len(self.plot):
            self.now_plot += 1
        if self.plot[self.now_plot] == "[toggle display]":
            self.display_on_mb = not self.display_on_mb
            self.mb_group.visible = not self.mb_group.visible
            self.label_group.visible = not self.label_group.visible
            self.now_plot += 1
        if self.display_on_mb:
            self.message.text = self.plot[self.now_plot]
        else:
            self.label_text = self.plot[self.now_plot]
            text = self._line_break_func(self.label_text, self.label.width)
            self.label.text = text

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self._next_plot()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == mouse.LEFT:
            self._next_plot()

    def on_resize(self, width, height):
        self.message.resize()
        self.label.position = (width // 2, height // 2, 0)
        self.label.width = 0.8 * width
        text = self._line_break_func(self.label_text, self.label.width)
        self.label.text = text

    def on_language_change(self):
        self.plot[:] = []
        self._load_plots()

    def on_scene_enter(self):
        self.now_plot = 0
        self.message.text = self.plot[0]


__all__ = "StartScene"
