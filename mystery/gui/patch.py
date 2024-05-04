from typing import Optional

from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage
from pyglet.sprite import Sprite


class ThreePatch:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        left: AbstractImage,
        middle: AbstractImage,
        right: AbstractImage,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._x, self._y = x, y
        self._width = width
        self._height = height
        self._sprites = []
        self._sprites.append(Sprite(left, batch=batch, group=group))
        self._sprites.append(Sprite(middle, batch=batch, group=group))
        self._sprites.append(Sprite(right, batch=batch, group=group))
        self._update()

    def __getitem__(self, key: int | slice) -> tuple[AbstractImage, ...]:
        if isinstance(key, int):
            return tuple([self._sprites[key].image])
        elif isinstance(key, slice):
            return tuple([sprite.image for sprite in self._sprites])
        else:
            raise ValueError("unsupported operation")

    def __setitem__(self, key: int, value: AbstractImage | tuple[AbstractImage, ...]):
        if isinstance(key, int) and isinstance(value, AbstractImage):
            self._sprites[key].image = value
        elif isinstance(key, slice):
            for i in [0, 1, 2][key]:
                self._sprites[i].image = value[i]
        else:
            raise ValueError("unsupported operation")
        self._update()

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x
        self._update()

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y
        self._update()

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width
        self._update()

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height
        self._update()

    @property
    def group(self) -> Group:
        return self._sprites[0].group

    @group.setter
    def group(self, group: Group):
        for sprite in self._sprites:
            sprite.group = group

    def _update(self):
        if 2 * self._height > self._width:
            raise ValueError("width should larger than twice of height")
        side_width = self._sprites[0].image.width
        side_height = self._sprites[0].image.height
        side_width *= self._height / side_height
        self._sprites[0].scale = self._height / side_height
        self._sprites[2].scale = self._height / side_height
        self._sprites[1].width = self._width - 2 * side_width
        self._sprites[1].height = self._height
        self._sprites[0].position = (self._x, self._y, 0)
        self._sprites[1].position = (self._x + side_width, self._y, 0)
        self._sprites[2].position = (self._x + self._width - side_width, self._y, 0)

    def draw(self):
        for sprite in self._sprites:
            sprite.draw()


class NinePatch:
    def __init__(self):
        pass


__all__ = "ThreePatch", "NinePatch"
