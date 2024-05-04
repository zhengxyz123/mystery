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

    def __getitem__(self, key: int | slice) -> tuple[Sprite, ...]:
        if isinstance(key, int):
            return tuple([self._sprites[key]])
        elif isinstance(key, slice):
            return self._sprites[key]
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

        corner_width = self._sprites[0].image.width
        corner_height = self._sprites[0].image.height
        corner_width *= self._height / corner_height

        self._sprites[0].scale = self._height / corner_height
        self._sprites[2].scale = self._height / corner_height
        self._sprites[1].width = self._width - 2 * corner_width
        self._sprites[1].height = self._height

        self._sprites[0].position = (self._x, self._y, 0)
        self._sprites[1].position = (self._x + corner_width, self._y, 0)
        self._sprites[2].position = (self._x + self._width - corner_width, self._y, 0)

    def draw(self):
        for sprite in self._sprites:
            sprite.draw()

    def update(
        self,
        *,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        self._update()


class NinePatch:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        # fmt: off
        tl: AbstractImage, tm: AbstractImage, tr: AbstractImage,
        ml: AbstractImage, mm: AbstractImage, mr: AbstractImage,
        bl: AbstractImage, bm: AbstractImage, br: AbstractImage,
        # fmt: on
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._scale = 1
        self._x, self._y = x, y
        self._width = width
        self._height = height
        self._sprites = {}
        self._sprites[(0, 0)] = Sprite(tl, batch=batch, group=group)
        self._sprites[(0, 1)] = Sprite(tm, batch=batch, group=group)
        self._sprites[(0, 2)] = Sprite(tr, batch=batch, group=group)
        self._sprites[(1, 0)] = Sprite(ml, batch=batch, group=group)
        self._sprites[(1, 1)] = Sprite(mm, batch=batch, group=group)
        self._sprites[(1, 2)] = Sprite(mr, batch=batch, group=group)
        self._sprites[(2, 0)] = Sprite(bl, batch=batch, group=group)
        self._sprites[(2, 1)] = Sprite(bm, batch=batch, group=group)
        self._sprites[(2, 2)] = Sprite(br, batch=batch, group=group)
        self._update()

    def __getitem__(self, key: tuple[int, ...]) -> Sprite:
        return self._sprites[key]

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float):
        self._scale = scale
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
        for coord in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            self._sprites[coord].scale = self._scale

        top_width = self._sprites[(0, 0)].width
        top_height = self._sprites[(0, 0)].height
        bottom_width = self._sprites[(2, 0)].width
        bottom_height = self._sprites[(2, 0)].height
        middle_width = self._width - 2 * top_width
        middle_height = self._height - top_height - bottom_height

        self._sprites[(0, 1)].width = self._sprites[(2, 1)].width = middle_width
        self._sprites[(0, 1)].height = top_height
        self._sprites[(2, 1)].height = bottom_height

        self._sprites[(1, 0)].width = self._sprites[(1, 2)].width = top_width
        self._sprites[(1, 0)].height = self._sprites[(1, 2)].height = middle_height
        self._sprites[(1, 1)].width = middle_width
        self._sprites[(1, 1)].height = middle_height

        self._sprites[(2, 0)].position = (self._x, self._y, 0)
        self._sprites[(2, 1)].position = (self._x + bottom_width, self._y, 0)
        self._sprites[(2, 2)].position = (
            self._x + bottom_width + middle_width,
            self._y,
            0,
        )
        self._sprites[(1, 0)].position = (self._x, self._y + bottom_height, 0)
        self._sprites[(1, 1)].position = (
            self._x + bottom_width,
            self._y + bottom_height,
            0,
        )
        self._sprites[(1, 2)].position = (
            self._x + bottom_width + middle_width,
            self._y + bottom_height,
            0,
        )
        self._sprites[(0, 0)].position = (
            self._x,
            self._y + bottom_height + middle_height,
            0,
        )
        self._sprites[(0, 1)].position = (
            self._x + top_width,
            self._y + bottom_height + middle_height,
            0,
        )
        self._sprites[(0, 2)].position = (
            self._x + top_width + middle_width,
            self._y + bottom_height + middle_height,
            0,
        )

    def draw(self):
        for sprite in self._sprites.values():
            sprite.draw()

    def update(
        self,
        *,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        self._update()


__all__ = "ThreePatch", "NinePatch"
