from importlib import import_module
from typing import Optional

from pyglet import clock
from pyglet.graphics import Batch

from mystery.character import Character
from mystery.gui.hud import KeyHint
from mystery.scene import GameWindow, Scene


class GameScene(Scene):
    def __init__(self, window: GameWindow):
        super().__init__(window)
        self.batch = Batch()
        self.character = Character(self)
        self.key_hint = KeyHint(self, self.batch)
        self._cached_room = {}
        self._now_room = None

    def switch_room(self, namespace: str, class_name: str, name: Optional[str] = None):
        """Load then switch to a room.

        The 3 parameters are:
          - namespace: load module at namespace `mystery.room.<namespace>`
          - class_name: load a class named `<class_name>Room` in the above namespace
          - name: a str refers to the instance of above class

        The default value of `name` is the lower case of `class_name`.
        """
        if not name:
            name = class_name.lower()
        if name not in self._cached_room:
            module = import_module(f"mystery.room.{namespace}")
            room = getattr(module, f"{class_name}Room")
            self._cached_room[name] = room(self, self.character)
        if self._now_room:
            self._now_room.dispatch_event("on_room_leave")
        self._now_room = self._cached_room[name]
        self.character.room = self._now_room
        self._now_room.dispatch_event("on_room_enter")

    def on_draw(self):
        self.window.clear()
        if self._now_room:
            self._now_room.draw()
        self.batch.draw()

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        self.window.push_handlers(self.key_hint)
        clock.schedule_interval(self.character.update, 4 / self.window.setting["fps"])
        self.switch_room("start", "Start")

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)
        self.window.remove_handlers(self.key_hint)
        if self._now_room:
            self._now_room.dispatch_event("on_room_leave")


__all__ = ("GameScene",)
