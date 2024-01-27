from __future__ import annotations

from typing import Dict

from pyglet.event import EventDispatcher
from pyglet.image import get_buffer_manager
from pyglet.window import Window, key

from mystery import resource, setting
from mystery.gui import WidgetFrame


class Scene(EventDispatcher):
    """A scene that is used to render different parts of the game."""

    def __init__(self, window: GameWindow):
        self.window = window
        self.frame = WidgetFrame(self.window)
        self.language = self.window.resource.language

    def on_language_change(self):
        """The callback function on changing the language."""
        pass

    def on_scene_enter(self):
        """The callback function on entering the scene."""
        pass

    def on_scene_leave(self):
        """The callback function when leaving the scene."""
        pass


Scene.register_event_type("on_language_change")
Scene.register_event_type("on_scene_enter")
Scene.register_event_type("on_scene_leave")


class GameWindow(Window):
    """Game main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption("Mystery")
        self.set_minimum_size(768, 576)
        self._scenes: Dict[str, Scene] = {}
        self._now = ""
        self.resource = resource
        self.setting = setting

    @property
    def scene(self) -> str:
        return self._now

    @scene.setter
    def scene(self, name: str):
        self.switch_scene(name)

    def add_scene(self, name: str, scene: Scene):
        """Add a scene."""
        self._scenes[name] = scene(self)

    def has_scene(self, name: str) -> bool:
        """Whether a scene is added."""
        return name in self._scenes

    def remove_scene(self, name: str):
        """
        Remove a scene.

        You cannot remove the active one!
        """
        if self._now == name:
            return
        del self._scenes[name]

    def switch_scene(self, name: str):
        """Switch to another scene."""
        if name not in self._scenes:
            raise NameError(f"scene '{name}' not found")
        # Close the old one.
        if self._now != "":
            self._scenes[self._now].frame.enable = False
            self._scenes[self._now].dispatch_event("on_scene_leave")
            self.remove_handlers(self._scenes[self._now])
        # Switch to the new one.
        self._now = name
        self._scenes[self._now].frame.enable = True
        if self._scenes[self._now].language != self.resource.language:
            self._scenes[self._now].dispatch_event("on_language_change")
            self._scenes[self._now].language = self.resource.language
        if hasattr(self._scenes[self._now], "on_resize"):
            self._scenes[self._now].on_resize(self.width, self.height)
        # Use a little trick to move the mouse slightly.
        # If the scene switches immediately after the button is pressed
        # (actually released), the button will remain hover until the
        # next time the scene switches back to the scene while moving
        # the mouse, and the state of the button will be recalculated.
        # By using this trick, the state of widgets can be recalculated
        # without physically moving the mouse.
        self._scenes[self._now].frame.on_mouse_motion(
            self._mouse_x, self._mouse_y, 1, 1
        )
        self._scenes[self._now].dispatch_event("on_scene_enter")
        self.push_handlers(self._scenes[self._now])

    def on_key_press(self, symbol, modifiers):
        if symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)
            if not self.fullscreen:
                self.set_minimum_size(768, 576)


__all__ = "Scene", "GameWindow"
