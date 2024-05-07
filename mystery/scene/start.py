from importlib import import_module
from textwrap import dedent

from pyglet.graphics import Batch, Group
from pyglet.text import Label
from pyglet.window import key, mouse

from mystery import utils
from mystery.gui.widgets import MessageBox
from mystery.resource.manager import FONT_NAME
from mystery.scene import GameWindow, Scene


class StartScene(Scene):
    def __init__(self, window: GameWindow):
        super().__init__(window)
        self._batch = Batch()
        self._mb_group = Group(order=0)
        self._now_plot = 0
        self._plot = []
        self._load_plots()

        self.message = MessageBox(self.window, self._batch, self._mb_group)
        self.frame.add_widget(self.message)

    def _load_plots(self):
        i = 0
        while True:
            trans_key = f"start.plot.{i}"
            text = self.window.resource.translate(trans_key)
            if text == trans_key:
                break
            else:
                self._plot.append(text)
                i += 1

    def _next_plot(self):
        if self._now_plot + 1 >= len(self._plot):
            if not self.window.has_scene("game"):
                game_scene = import_module("mystery.scene.game").GameScene
                self.window.add_scene("game", game_scene)
            self.window.switch_scene("game")
        if self._now_plot + 1 < len(self._plot):
            self._now_plot += 1
        self.message.text = self._plot[self._now_plot]

    def on_draw(self):
        self.window.clear()
        self._batch.draw()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self._next_plot()
        elif symbol == key.ESCAPE:
            self.window.switch_scene("menu")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons == mouse.LEFT:
            self._next_plot()

    def on_resize(self, width, height):
        self.message.resize()

    def on_language_change(self):
        self._plot[:] = []
        self._load_plots()

    def on_scene_enter(self):
        self._now_plot = 0
        self.message.text = self._plot[0]


__all__ = ("StartScene",)
