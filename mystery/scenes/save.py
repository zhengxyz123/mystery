from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite

from mystery.gui.widgets import AdvancedFrame
from mystery.scenes import Scene


class SaveLoadScene(Scene):
    def __init__(self, window: "mystery.scenes.GameWindow"):
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

        self.select_frame = AdvancedFrame(
            self.window.resource.translate("save.load.title"),
            self.window.width // 2 - 350,
            self.window.height // 2 - 250,
            700,
            500,
            batch=self.batch,
            group=self.mid_group,
        )
        self.select_frame.push_handlers(
            on_button_click=lambda: self.window.switch_scene("menu")
        )
        self.frame.add_widget(self.select_frame)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_resize(self, width, height):
        self.background.position = (width // 2, height // 2, 0)
        if 3 * width >= 4 * height:
            self.background.scale = width / self.background.image.width
        else:
            self.background.scale = height / self.background.image.height
        self.select_frame.position = (width // 2 - 350, height // 2 - 250)

    def on_language_change(self):
        self.select_frame.title = self.window.resource.translate("save.load.title")


__all__ = ("SaveLoadScene",)
