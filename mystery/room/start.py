from typing import Optional

from pyglet.graphics import Group
from pyglet.window import key

from mystery.character import Character, CharacterDirection, CharacterState
from mystery.entity.campfire import CampfireEntity
from mystery.gui.hud import KeyHint
from mystery.gui.widgets import MessageBox
from mystery.room.base import BaseRoom
from mystery.scene.game import GameScene


class StartRoom(BaseRoom):
    def __init__(
        self,
        game: GameScene,
        character: Character,
        group: Optional[Group] = None,
    ):
        super().__init__(game, "start", character, group)
        self.key_hint_group = Group(order=0)
        self.key_hint = KeyHint(self.gui_batch, self.key_hint_group)
        self.mb_group = Group(order=1)
        self.message_box = MessageBox(self.game.window, self.gui_batch, self.mb_group)
        self.campfire = CampfireEntity(self.game, self)

        self.plots = []
        self._now_plot = 0
        self.data = {
            "state": -1,
        }

    def _load_plots(self):
        i = 0
        while True:
            trans_key = f"room.start.plot.{i}"
            text = self.game.window.resource.translate(trans_key)
            if text == trans_key:
                break
            else:
                self.plots.append(text)
                i += 1

    def _next_plot(self):
        if self._now_plot + 1 >= len(self.plots):
            self._switch_state()
        if self._now_plot + 1 < len(self.plots):
            self._now_plot += 1
        self.message_box.text = self.plots[self._now_plot]

    def _switch_state(self):
        if self.data["state"] == 0:
            self.data["state"] = 1
            self.key_hint_group.visible = True
            self.mb_group.visible = False
            self.character.state = CharacterState.IDLE

    def interact(self):
        if self.check_collide("campfire"):
            self.campfire.dispatch_event("on_interact")

    def on_key_release(self, symbol, modifiers):
        if self.data["state"] == 0:
            if symbol == key.SPACE:
                self._next_plot()

    def on_resize(self, width, height):
        self.message_box.resize()

    def on_room_enter(self, *args):
        self._load_map()
        self.key_hint_group.visible = False
        self.mb_group.visible = True
        self.key_hint.reset()
        self.character.direction = CharacterDirection.UP
        self.character.state = CharacterState.FREEZE
        self.character.position = self._spawn_points["start"]
        self.data["state"] = 0
        self.plots[:] = []
        self._now_plot = 0
        self._load_plots()
        self.message_box.text = self.plots[0]
        self.game.window.push_handlers(self)

    def on_room_leave(self):
        self.game.window.remove_handlers(self)


__all__ = ("StartRoom",)
