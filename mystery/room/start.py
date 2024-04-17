from typing import Optional

from pyglet.graphics import Group

from mystery.character import Character, CharacterDirection
from mystery.entity.cup import CupEntity
from mystery.room.base import BaseRoom
from mystery.scene.game import GameScene


class StartRoom(BaseRoom):
    def __init__(
        self,
        game: GameScene,
        char: Character,
        group: Optional[Group] = None,
    ):
        super().__init__(game, "example", char, group)
        self.cup = CupEntity(self._game)

    def interact(self):
        if self.check_collide("cup"):
            self.cup.dispatch_event("on_interact")

    def on_room_enter(self, *args):
        self._load_map()
        self.char.position = self._spawn_points["start"]
        self.char.direction = CharacterDirection.UP


__all__ = ("StartRoom",)
