from typing import Optional

from pyglet.graphics import Group

from mystery.character import Character, CharacterDirection
from mystery.rooms.base import BaseRoom


class StartRoom(BaseRoom):
    def __init__(
        self,
        game: "mystery.scenes.game.GameScene",
        char: Character,
        group: Optional[Group] = None,
    ):
        super().__init__(game, "example", char, group)

    def interact(self):
        if self.check_collide("cup"):
            pass

    def on_room_enter(self, *args):
        self._load_map()
        self.char.position = self._spawn_points["start"]
        self.char.direction = CharacterDirection.UP


__all__ = ("StartRoom",)
