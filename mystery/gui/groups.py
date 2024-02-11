from typing import Optional, Tuple

from pyglet import gl
from pyglet.graphics import Group


class ScissorGroup(Group):
    """A Custom Group that defines a "Scissor" area.

    From pyglet's example.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        order: int = 0,
        parent: Optional[Group] = None,
    ):
        super().__init__(order, parent)
        self._x, self._y = x, y
        self._width, self._height = width, height

    @property
    def area(self) -> Tuple[int, ...]:
        return self._x, self._y, self._width, self._height

    @area.setter
    def area(self, area: Tuple[int, ...]):
        self._x, self._y, self._width, self._height = area

    def set_state(self):
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(self._x, self._y, self._width, self._height)

    def unset_state(self):
        gl.glDisable(gl.GL_SCISSOR_TEST)


__all__ = ("ScissorGroup",)
