from importlib import import_module

from pyglet import clock
from pyglet.graphics import Batch

from mystery.character import Character
from mystery.gui.hud import KeyHint
from mystery.scenes import Scene


class GameScene(Scene):
    def __init__(self, window: "mystery.scenes.GameWindow"):
        super().__init__(window)
        self.batch = Batch()
        self.character = Character(self)
        self.key_hint = KeyHint(self, self.batch)
        self._cached_room = {}
        self._now_room = None

    def switch_room(self, name: str):
        if name not in self._cached_room:
            module = import_module(f"mystery.rooms.{name}")
            room = getattr(module, f"{name.capitalize()}Room")
            self._cached_room[name] = room(self, self.character)
        self._now_room = self._cached_room[name]
        self.character.room = self._now_room
        self._now_room.dispatch_event("on_room_enter")

    def on_draw(self):
        self.window.clear()
        if self._now_room is not None:
            self._now_room.draw()
        self.batch.draw()

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        self.window.push_handlers(self.key_hint)
        clock.schedule_interval(self.character.update, 4 / self.window.setting["fps"])
        self.key_hint.reset()
        self.switch_room("start")

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)
        self.window.remove_handlers(self.key_hint)
        if self._now_room is not None:
            self._now_room.dispatch_event("on_room_leave")


__all__ = ("GameScene",)
