from typing import Optional, Tuple

from pyglet.graphics import Batch, Group
from pyglet.image import load as load_image
from pyglet.sprite import Sprite
from pyglet.window import Window

from mystery import resource
from mystery.gui.groups import ScissorGroup
from mystery.gui.widgets import WidgetBase

pages_texture = []
for i in range(1, 8):
    page_file = resource.loader.file(f"textures/gui/book/flip_pages_{i}.png")
    img = load_image("example.png", page_file)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    pages_texture.append(img)


class Book(WidgetBase):
    """A book with flipping animation."""

    def __init__(
        self,
        window: Window,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._window = window
        width, height = 500, 350
        x, y = (self._window.width - width) // 2, (self._window.height + height) // 2
        super().__init__(x, y, width, height)

        self.page_group = Group(order=0, parent=group)
        self.page = Sprite(
            img=pages_texture[0],
            x=self._window.width // 2,
            y=self._window.height // 2,
            batch=batch,
        )
        self.text_group = []
        for _ in range(4):
            self.text_group.append(ScissorGroup(0, 0, 0, 0, order=1, parent=group))

    def _update_position(self):
        width, height = self._window.get_size()
        self.page.position = width // 2, height // 2, 0

    def draw(self):
        self.page.draw()

    def resize(self):
        self.position = (self._window.width - self._width) // 2, (
            self._window.height + self._height
        ) // 2


__all__ = "Book"
