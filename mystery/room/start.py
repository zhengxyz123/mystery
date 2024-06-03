from typing import Optional

from pyglet.graphics import Group

from mystery.character import Character, CharacterDirection
from mystery.entity.cup import CupEntity
from mystery.gui.hud import KeyHint
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

        self.key_hint_group = Group(order=0)
        self.cup_group = Group(order=1)
        self.cup_group.visible = False

        self.key_hint = KeyHint(self.gui_batch, self.key_hint_group)
        self.cup = CupEntity(self._game, self)

    def interact(self):
        if self.check_collide("cup"):
            self.key_hint._state = 2
            self.key_hint.update2(0)
            self.cup.dispatch_event("on_interact")

    def on_room_enter(self, *args):
        self._load_map()
        self.char.position = self._spawn_points["start"]
        self.char.direction = CharacterDirection.UP
        self.key_hint.reset()
        self._game.window.push_handlers(self.key_hint)

    def on_rome_leave(self, *args):
        self._game.window.remove_handlers(self.key_hint)


__all__ = ("StartRoom",)
