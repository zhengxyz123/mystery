from pyglet.graphics import Batch
from pyglet.window import key

from mystery.character import CharacterState
from mystery.entity.base import EntityBase
from mystery.gui.widgets import MessageBox
from mystery.scene.game import GameScene


class CupEntity(EntityBase):
    def __init__(self, game: GameScene, room: "mystery.room.base.BaseRoom"):
        super().__init__(game, room)
        self._interacting = False
        self.message = MessageBox(
            self.game.window, self.room.gui_batch, self.room.cup_group
        )
        self.message.text = "This is a cup."

    def on_interact(self):
        if self._interacting:
            return
        self._interacting = True
        self.room.cup_group.visible = True
        self.on_resize(self.game.window.width, self.game.window.height)
        self.game.character.state = CharacterState.CTRLED
        self.game.window.remove_handlers(self.game.character)
        self.game.window.push_handlers(self)

    def on_key_release(self, symbol, modifiers):
        if not self._interacting:
            return
        if symbol == key.SPACE:
            self._interacting = False
            self.room.cup_group.visible = False
            self.game.character.state = CharacterState.IDLE
            self.game.window.remove_handlers(self)
            self.game.window.push_handlers(self.game.character)

    def on_resize(self, width, height):
        self.message.resize()


__all__ = ("CupEntity",)
