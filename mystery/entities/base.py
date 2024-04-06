from pyglet.event import EventDispatcher


class EntityBase(EventDispatcher):
    def __init__(self):
        pass

    def on_interact(self):
        pass


EntityBase.register_event_type("on_interact")


__all__ = ("EntityBase",)
