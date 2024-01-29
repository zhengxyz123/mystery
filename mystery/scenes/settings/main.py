from importlib import import_module

from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.window import Window

from mystery.gui.widgets import AdvancedFrame, TextButton
from mystery.scenes import Scene


class SettingsScene(Scene):
    def __init__(self, window: Window):
        super().__init__(window)
        self.batch = Batch()
        self.back_group = Group(order=0)
        self.mid_group = Group(order=1)
        self.fore_group = Group(order=2)

        self.background_image = self.window.resource.loader.image(
            "textures/background.png"
        )
        self.background_image.anchor_x = self.background_image.width // 2
        self.background_image.anchor_y = self.background_image.height // 2
        self.background = Sprite(
            self.background_image,
            x=self.window.width // 2,
            y=self.window.height // 2,
            batch=self.batch,
            group=self.back_group,
        )

        self.buttons_frame = AdvancedFrame(
            self.window.resource.translate("settings.title"),
            self.window.width // 2 - 140,
            self.window.height // 2 - 95,
            280,
            268,
            batch=self.batch,
            group=self.mid_group,
        )
        self.graphic_button = TextButton(
            self.window.resource.translate("settings.graphic"),
            self.window.width // 2 - 120,
            self.window.height // 2 + 32,
            240,
            55,
            batch=self.batch,
            group=self.fore_group,
        )
        self.sound_button = TextButton(
            self.window.resource.translate("settings.sound"),
            self.window.width // 2 - 120,
            self.window.height // 2 - 28,
            240,
            55,
            batch=self.batch,
            group=self.fore_group,
        )
        self.language_button = TextButton(
            self.window.resource.translate("settings.language"),
            self.window.width // 2 - 120,
            self.window.height // 2 - 88,
            240,
            55,
            batch=self.batch,
            group=self.fore_group,
        )
        self.buttons_frame.push_handlers(
            on_button_click=lambda: self.window.switch_scene("menu")
        )
        self.language_button.push_handlers(on_click=lambda: self.goto("language"))
        self.frame.add_widget(
            self.buttons_frame,
            self.graphic_button,
            self.sound_button,
            self.language_button,
        )

    def goto(self, name: str):
        scene_name = f"settings.{name}"
        if not self.window.has_scene(scene_name):
            module = import_module(f"mystery.scenes.settings.{name}")
            next_scene = getattr(module, f"{name.title()}SettingScene")
            self.window.add_scene(scene_name, next_scene)
        self.window.switch_scene(scene_name)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_resize(self, width, height):
        self.background.position = (width // 2, height // 2, 0)
        if 3 * width >= 4 * height:
            self.background.scale = width / self.background.image.width
        else:
            self.background.scale = height / self.background.image.height
        self.buttons_frame.position = (width // 2 - 140, height // 2 - 110)
        self.graphic_button.position = (width // 2 - 120, height // 2 + 32)
        self.sound_button.position = (width // 2 - 120, height // 2 - 28)
        self.language_button.position = (width // 2 - 120, height // 2 - 88)

    def on_language_change(self):
        self.buttons_frame.title = self.window.resource.translate("settings.title")
        self.graphic_button.text = self.window.resource.translate("settings.graphic")
        self.sound_button.text = self.window.resource.translate("settings.sound")
        self.language_button.text = self.window.resource.translate("settings.language")


__all__ = "SettingsScene"
