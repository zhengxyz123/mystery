from enum import StrEnum
from typing import Tuple

from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.image import Animation, AnimationFrame, ImageGrid
from pyglet.sprite import Sprite
from pyglet.window import Window, key

from mystery import resmgr

idle_img = resmgr.loader.image("textures/character/idle.png")
idle_seq = ImageGrid(idle_img, 4, 3).get_texture_sequence()
run_img = resmgr.loader.image("textures/character/run.png")
run_seq = ImageGrid(run_img, 4, 8).get_texture_sequence()
sit_img = resmgr.loader.image("textures/character/sit.png")
sit_seq = ImageGrid(sit_img, 4, 3).get_texture_sequence()
walk_img = resmgr.loader.image("textures/character/walk.png")
walk_seq = ImageGrid(walk_img, 4, 8).get_texture_sequence()

char_anime = {
    "idle": {},
    "run": {},
    "sit": {},
    "walk": {},
}
# Idle animations.
for n, direction in enumerate(["right", "down", "left", "up"]):
    frame1 = AnimationFrame(idle_seq[(n, 0)], 0.4)
    frame2 = AnimationFrame(idle_seq[(n, 1)], 0.1)
    frame3 = AnimationFrame(idle_seq[(n, 2)], 0.4)
    char_anime["idle"][direction] = Animation([frame1, frame2, frame3, frame2])
# Run and walk animations.
for state, seq in {"run": run_seq, "walk": walk_seq}.items():
    for m, direction in enumerate(["right", "down", "left", "up"]):
        all_frames = []
        for n in range(8):
            frame = AnimationFrame(seq[(m, n)], 0.0625)
            all_frames.append(frame)
        char_anime[state][direction] = Animation(all_frames)


class CharcterState(StrEnum):
    CTRLED = "controlled"
    IDLE = "idle"
    RUN = "run"
    SIT = "sit"
    WALK = "walk"


class CharcterDirection(StrEnum):
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"
    UP = "up"


class Charcter(EventDispatcher):
    def __init__(self, window: Window, batch: Batch, group: Group):
        self._window = window
        self._batch = batch
        self._group = Group(parent=group)
        self._sprite = Sprite(
            char_anime["idle"]["up"], batch=self._batch, group=self._group
        )

        self._state = CharcterState.IDLE
        self._direction = CharcterDirection.UP
        self._runnable = False
        self._prev_state = None
        self._prev_direction = None
        self._mapping = {
            key.RIGHT: CharcterDirection.RIGHT,
            key.DOWN: CharcterDirection.DOWN,
            key.LEFT: CharcterDirection.LEFT,
            key.UP: CharcterDirection.UP,
        }

    @property
    def state(self) -> CharcterState:
        return self._state

    @state.setter
    def state(self, state: CharcterState):
        assert isinstance(state, CharcterState)
        self._state = state

    @property
    def direction(self) -> CharcterDirection:
        return self._direction

    @direction.setter
    def direction(self, direction: CharcterDirection):
        assert isinstance(direction, CharcterDirection)
        self._direction = direction

    @property
    def position(self) -> Tuple[int]:
        return self._sprite.position

    @position.setter
    def position(self, pos: Tuple[int]):
        self._sprite.position = pos

    def on_key_press(self, symbol, modifiers):
        if self._state == CharcterState.CTRLED:
            return
        if symbol == key.ESCAPE:
            self._window.switch_scene("menu")
        elif symbol == key.LSHIFT:
            self._runnable = True
        elif key.LEFT <= symbol <= key.DOWN:
            self._direction = self._mapping[symbol]
            self._state = CharcterState.WALK
        if self._runnable and self._state == CharcterState.WALK:
            self._state = CharcterState.RUN

    def on_key_release(self, symbol, modifiers):
        if self._state == CharcterState.CTRLED:
            return
        if symbol == key.LSHIFT:
            self._runnable = False
            if self._state == CharcterState.RUN:
                self._state = CharcterState.WALK
        elif key.LEFT <= symbol <= key.DOWN:
            if self._mapping[symbol] == self._direction:
                self._state = CharcterState.IDLE

    def update(self, dt: float):
        if self._prev_state != self._state or self._prev_direction != self._direction:
            state = self._prev_state = self._state.value
            direction = self._prev_direction = self._direction.value
            self._sprite.image = char_anime[state][direction]


__all__ = "CharcterState", "CharcterDirection", "Charcter"
