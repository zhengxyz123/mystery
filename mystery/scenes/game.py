from pyglet import clock
from pyglet.graphics import Batch, Group
from pyglet.window import Window

from mystery.charcter import Charcter
from mystery.scenes import Scene


class GameScene(Scene):
    def __init__(self, window: Window):
        super().__init__(window)
        self.batch1 = Batch()
        self.batch2 = Batch()
        self.back_group = Group(order=0)
        self.char_group = Group(order=1)
        self.fore_group = Group(order=2)
        self.hud_group = Group(order=3)

        self.character = Charcter(window, self.batch1, self.char_group)

    def on_draw(self):
        self.window.clear()
        self.batch1.draw()

    def on_resize(self, width, height):
        self.character.position = (width // 2 - 32, height // 2 - 32, 0)

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        clock.schedule_interval(self.character.update, 1 / self.window.setting["fps"])

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)


__all__ = "GameScene"
