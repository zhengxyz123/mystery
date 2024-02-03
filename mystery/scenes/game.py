from pyglet import clock
from pyglet.graphics import Batch, Group
from pyglet.window import Window, key

from mystery.charcter import Charcter
from mystery.gui.keyhint import KeyHint
from mystery.scenes import Scene


class GameScene(Scene):
    def __init__(self, window: Window):
        super().__init__(window)
        self.batch = Batch()
        self.back_group = Group(order=0)
        self.char_group = Group(order=1)
        self.fore_group = Group(order=2)
        self.hud_group = Group(order=3)
        self._triggered = False

        self.character = Charcter(self.window, self.batch, self.char_group)
        self.key_hint = KeyHint(self.window, self.batch, self.hud_group)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if key.LEFT <= symbol <= key.DOWN and not self._triggered:
            clock.schedule_once(self.key_hint.update1, 5)
            self._triggered = True

    def on_resize(self, width, height):
        self.character.position = (width // 2 - 32, height // 2 - 32, 0)

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        clock.schedule_interval(self.character.update, 4 / self.window.setting["fps"])
        self.key_hint.reset()

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)


__all__ = "GameScene"
