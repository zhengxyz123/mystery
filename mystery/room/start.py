from typing import Optional

from pyglet.graphics import Group

from mystery.character import Character, CharacterDirection
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
        super().__init__(game, "start", char, group)
        self.key_hint_group = Group(order=0)
        self.key_hint = KeyHint(self.gui_batch, self.key_hint_group)
    
    def _update_iobjs(self):
        super()._update_iobjs()
        tent_0 = self.ibojs_dict["tent_0"]
        cond = tent_0.y > self.char.position[1] + 4
        for name, iobj in self.ibojs_dict.items():
            if name.startswith("tent_"):
                if cond:
                    iobj.z = 0
                else:
                    iobj.z = 2

    def interact(self):
        pass

    def on_room_enter(self, *args):
        self._load_map()
        self.char.position = self._spawn_points["start"]
        self.char.direction = CharacterDirection.UP
        self.key_hint.reset()

    def on_rome_leave(self):
        pass


__all__ = ("StartRoom",)
