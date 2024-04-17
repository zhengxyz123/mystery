from pyglet.window import key

from mystery.character import CharacterState
from mystery.entity.base import EntityBase
from mystery.scene.game import GameScene


class CupEntity(EntityBase):
    def __init__(self, game: GameScene):
        super().__init__(game)
        self._interacting = False

    def on_interact(self):
        if self._interacting:
            return
        self._interacting = True
        self.game.character.state = CharacterState.CTRLED
        self.game.window.remove_handlers(self.game.character)
        self.game.window.push_handlers(self)

    def on_key_release(self, symbol, modifiers):
        if not self._interacting:
            return
        if symbol == key.SPACE:
            self._interacting = False
            self.game.character.state = CharacterState.IDLE
            self.game.window.remove_handlers(self)
            self.game.window.push_handlers(self.game.character)


__all__ = ("CupEntity",)
