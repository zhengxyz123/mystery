from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite

from mystery.gui.widgets import (
    AdvancedFrame,
    DecoratedButton,
    LanguageSelectOption,
    OptionGroup,
    ScrollableLayout,
    ScrollBar,
)
from mystery.resource.manager import SUPPORTED_LANG
from mystery.scene import Scene


class LanguageSettingScene(Scene):
    def __init__(self, window: "mystery.scenes.GameWindow"):
        super().__init__(window)
        self.batch = Batch()
        self.back_group = Group(order=0)
        self.mid_group = Group(order=1)
        self.fore_group = Group(order=2)
        self.options_group = OptionGroup()

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

        self.language_frame = AdvancedFrame(
            self.window.resource.translate("settings.language"),
            self.window.width // 2 - 300,
            self.window.height // 2 - 250,
            600,
            500,
            batch=self.batch,
            group=self.mid_group,
        )
        self.apply_button = DecoratedButton(
            self.window.resource.translate("general.apply"),
            self.window.width // 2 - 75,
            self.window.height // 2 - 270,
            150,
            batch=self.batch,
            group=self.fore_group,
        )
        self.options_layout = ScrollableLayout(
            self.window.width // 2 - 220,
            self.window.height // 2 - 210,
            440,
            390,
            group=self.fore_group,
        )
        self.scroll_bar = ScrollBar(
            self.window.width // 2 + 220,
            self.window.height // 2 - 210,
            390,
            scrollable_layout=self.options_layout,
            batch=self.batch,
            group=self.fore_group,
        )
        self.options_layout.content_height = len(SUPPORTED_LANG) * 50
        self.language_options = []
        for index, item in enumerate(SUPPORTED_LANG.items()):
            self.language_options.append(
                option := LanguageSelectOption(
                    self.window.width // 2 - 200,
                    self.window.height // 2 + 130 - 50 * index,
                    400,
                    40,
                    text=item[1],
                    value=item[0],
                    batch=self.batch,
                    group=self.fore_group,
                )
            )
            self.options_group.add(option)
            self.options_layout.add(option)
        self.language_frame.push_handlers(
            on_button_click=lambda: self.window.switch_scene("settings.main")
        )
        self.apply_button.push_handlers(on_click=self.apply_change)
        self.frame.add_widget(
            self.language_frame,
            self.apply_button,
            self.options_layout,
            self.scroll_bar,
        )

    def apply_change(self):
        self.window.setting["lang"] = self.options_group.value
        self.window.setting.save()
        self.window.resource.language = self.options_group.value
        self.dispatch_event("on_language_change")
        self.window.switch_scene("settings.main")

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_resize(self, width, height):
        self.background.position = (width // 2, height // 2, 0)
        if 3 * width >= 4 * height:
            self.background.scale = width / self.background.image.width
        else:
            self.background.scale = height / self.background.image.height
        self.language_frame.position = (width // 2 - 300, height // 2 - 250)
        self.apply_button.position = (width // 2 - 75, height // 2 - 270)
        self.options_layout.position = (width // 2 - 220, height // 2 - 210)
        self.scroll_bar.position = (width // 2 + 220, height // 2 - 210)
        for index, option in enumerate(self.language_options):
            position = self.options_layout.get_point(
                width // 2 - 200, height // 2 + 130 - 50 * index
            )
            option.position = position

    def on_language_change(self):
        self.language_frame.title = self.window.resource.translate("settings.language")
        self.apply_button.text = self.window.resource.translate("general.apply")

    def on_scene_enter(self):
        i = list(SUPPORTED_LANG.keys()).index(self.window.resource.language)
        if not (option := self.language_options[i]).selected:
            option.selected = True
        self.options_layout.offset_y = 0


__all__ = ("LanguageSettingScene",)
