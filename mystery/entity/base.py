from pyglet.event import EventDispatcher


class EntityBase(EventDispatcher):
    def __init__(
        self, game: "mystery.scene.game.GameScene", room: "mystery.room.base.BaseRoom"
    ):
        self.game = game
        self.room = room

    def on_interact(self):
        pass


EntityBase.register_event_type("on_interact")


__all__ = ("EntityBase",)
