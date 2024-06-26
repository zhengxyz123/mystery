from __future__ import annotations

from contextlib import contextmanager
from time import strftime

from pyglet.event import EventDispatcher
from pyglet.image import get_buffer_manager
from pyglet.math import Mat4
from pyglet.window import Window, key

from mystery import data_path, game_setting, resmgr
from mystery import version as mystery_ver
from mystery.gui.frame import WidgetFrame


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


Scene.register_event_type("on_resize")
Scene.register_event_type("on_language_change")
Scene.register_event_type("on_scene_enter")
Scene.register_event_type("on_scene_leave")


class GameWindow(Window):
    """Game main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption(f"Mystery {mystery_ver}")
        self.set_icon(resmgr.loader.image("textures/pyglet.png"))
        self.set_minimum_size(768, 576)
        self._scenes: dict[str, Scene] = {}
        self._now = ""
        self.resource = resmgr
        self.setting = game_setting

    @property
    def scene(self) -> str:
        return self._now

    @scene.setter
    def scene(self, name: str):
        self.switch_scene(name)

    @contextmanager
    def apply_view(self, view: Mat4):
        prev_view = self.view
        self.view = view
        try:
            yield
        finally:
            self.view = prev_view

    def add_scene(self, name: str, scene: type[Scene]):
        """Add a scene."""
        self._scenes[name] = scene(self)

    def has_scene(self, name: str) -> bool:
        """Whether a scene is added."""
        return name in self._scenes

    def remove_scene(self, name: str):
        """Remove a scene.

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
        self._scenes[self._now].dispatch_event("on_resize", self.width, self.height)
        self._scenes[self._now].frame.on_mouse_motion(
            self._mouse_x, self._mouse_y, 1, 1
        )
        self._scenes[self._now].dispatch_event("on_scene_enter")
        self.push_handlers(self._scenes[self._now])

    def on_key_press(self, symbol, modifiers):
        if symbol == key.F5:
            filename = data_path / "screenshots" / strftime("%Y%m%d_%H%M%S.png")
            if modifiers & key.MOD_SHIFT:
                get_buffer_manager().get_depth_buffer().save(filename)
            else:
                get_buffer_manager().get_color_buffer().save(filename)
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)
            if not self.fullscreen:
                self.set_minimum_size(768, 576)


__all__ = "Scene", "GameWindow"
