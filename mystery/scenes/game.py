from pyglet import clock
from pyglet.graphics import Batch

from mystery.character import Character
from mystery.gui.hud import KeyHint
from mystery.rooms import BaseRoom
from mystery.scenes import Scene


class GameScene(Scene):
    def __init__(self, window: "mystery.scenes.GameWindow"):
        super().__init__(window)
        self.batch = Batch()
        self.character = Character(self)
        self.key_hint = KeyHint(self, self.batch)
        self.room = BaseRoom(self, self.character)

    def on_draw(self):
        self.window.clear()
        self.room.draw()
        self.batch.draw()

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        self.window.push_handlers(self.key_hint)
        clock.schedule_interval(self.character.update, 4 / self.window.setting["fps"])
        self.key_hint.reset()
        self.room.dispatch_event("on_room_enter")

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)
        self.window.remove_handlers(self.key_hint)


__all__ = ("GameScene",)
