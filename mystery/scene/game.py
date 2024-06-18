from importlib import import_module
from typing import Optional

from pyglet import clock
from pyglet.graphics import Batch

from mystery.character import Character
from mystery.scene import GameWindow, Scene

rooms = {
    "start": ("start", "StartRoom"),
    "start_tent": ("start", "StartTentRoom"),
}


class GameScene(Scene):
    def __init__(self, window: GameWindow):
        super().__init__(window)
        self._batch = Batch()
        self._cached_room = {}
        self._now_room = None
        self.character = Character(self)

    def switch_room(self, room_name: str, *args):
        """Load then switch to a room."""
        module_name, class_name = rooms[room_name]
        if room_name not in self._cached_room:
            module = import_module(f"mystery.room.{module_name}")
            room = getattr(module, class_name)
            self._cached_room[room_name] = room(self, self.character)
        if self._now_room:
            self._now_room.dispatch_event("on_room_leave")
        self._now_room = self._cached_room[room_name]
        self.character.batch = self._now_room.map_batches["char"]
        self.character.room = self._now_room
        self._now_room.dispatch_event("on_room_enter", *args)

    def on_draw(self):
        self.window.clear()
        if self._now_room is not None:
            self._now_room.draw()
        self._batch.draw()

    def on_scene_enter(self):
        self.window.push_handlers(self.character)
        clock.schedule_interval(self.character.update, 4 / self.window.setting["fps"])
        self.switch_room("start", "start_game")

    def on_scene_leave(self):
        clock.unschedule(self.character.update)
        self.window.remove_handlers(self.character)
        if self._now_room:
            self._now_room.dispatch_event("on_room_leave")


__all__ = ("GameScene",)
