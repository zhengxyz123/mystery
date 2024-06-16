from pyglet.window import key

from mystery.character import CharacterState
from mystery.entity.base import EntityBase


class CampfireEntity(EntityBase):
    def __init__(self, game, room):
        super().__init__(game, room)
        self.plots = []
        self._now_plot = 0
        self._interacting = False
        self._show_hints = self.room.key_hint_group.visible
        self._language = ""

    def _load_plots(self):
        i = 0
        while True:
            trans_key = f"room.start.campfire.plot.{i}"
            text = self.game.window.resource.translate(trans_key)
            if text == trans_key:
                break
            else:
                self.plots.append(text)
                i += 1

    def _next_plot(self):
        if self._now_plot + 1 >= len(self.plots):
            self.room.character.state = CharacterState.IDLE
            self.room.key_hint_group.visible = self._show_hints
            self.room.mb_group.visible = False
            self.game.window.remove_handlers(self)
            self.game.window.push_handlers(self.room.character)
            self._interacting = False
        if self._now_plot + 1 < len(self.plots):
            self._now_plot += 1
        self.room.message_box.text = self.plots[self._now_plot]

    def on_interact(self):
        if self._interacting:
            return
        self._interacting = True
        self._show_hints = self.room.key_hint_group.visible
        self._now_plot = 0
        if self._language != self.game.window.resource.language:
            self.plots[:] = []
            self._load_plots()
            self._language = self.game.window.resource.language
        self.room.character.state = CharacterState.FREEZE
        self.room.key_hint_group.visible = False
        self.room.mb_group.visible = True
        self.room.message_box.text = self.plots[0]
        self.game.window.remove_handlers(self.room.character)
        self.game.window.push_handlers(self)

    def on_key_release(self, symbol, modifiers):
        if not self._interacting:
            return
        if symbol == key.SPACE:
            self._next_plot()


__all__ = ("CampfireEntity",)
