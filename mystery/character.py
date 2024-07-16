from enum import StrEnum
from typing import Optional

from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.image import Animation, AnimationFrame, ImageGrid
from pyglet.math import Vec2
from pyglet.window import key

from mystery import resmgr
from mystery.depth_sprite import DepthSprite as Sprite

idle_img = resmgr.loader.image("textures/character/idle.png")
idle_seq = ImageGrid(idle_img, 4, 3).get_texture_sequence()
run_img = resmgr.loader.image("textures/character/run.png")
run_seq = ImageGrid(run_img, 4, 8).get_texture_sequence()
sit_img = resmgr.loader.image("textures/character/sit.png")
sit_seq = ImageGrid(sit_img, 4, 3).get_texture_sequence()
walk_img = resmgr.loader.image("textures/character/walk.png")
walk_seq = ImageGrid(walk_img, 4, 8).get_texture_sequence()
bubble_img = resmgr.loader.image("textures/character/bubble.png")
bubble_seq = ImageGrid(bubble_img, 4, 8).get_texture_sequence()

char_anime = {
    "idle": {},
    "run": {},
    "sit": {},
    "walk": {},
}
bubble_anime = {}
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
# Bubble animations.
for i, state in enumerate(["question", "exclamation", "dots", "love"]):
    all_frames = []
    for j in range(8):
        duration = 0.1 if j < 7 else 1
        frame = AnimationFrame(bubble_seq[(i, j)], duration)
        all_frames.append(frame)
    bubble_anime[state] = Animation(all_frames)


class CharacterDirection(StrEnum):
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"
    UP = "up"


class CharacterBubble(StrEnum):
    EMPTY = "empty"
    LOVE = "love"
    DOTS = "dots"
    EXCLAMATION = "exclamation"
    QUESTION = "question"


class CharacterState(StrEnum):
    FREEZE = "freeze"
    IDLE = "idle"
    RUN = "run"
    SIT = "sit"
    WALK = "walk"


class Character(EventDispatcher):
    def __init__(
        self,
        game: "mystery.scene.game.GameScene",
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
    ):
        self._game = game
        self._batch = batch
        self._group = Group(parent=group)
        self._char_sprite = Sprite(
            char_anime["idle"]["up"], 0, 0, 1, batch=self._batch, group=self._group
        )
        self._bubble_sprite = Sprite(
            bubble_anime["dots"],
            self._char_sprite.x + 30,
            self._char_sprite.y + 50,
            1,
            batch=self._batch,
            group=self._group,
        )
        self._bubble_sprite.visible = False
        self._bubble_sprite.set_handler("on_animation_end", self._reset_bubble)

        self._state = CharacterState.IDLE
        self._direction = CharacterDirection.UP
        self._bubble = CharacterBubble.EMPTY
        self._runnable = False
        self._room = None
        self._prev_state = None
        self._prev_direction = None
        self._prev_emotion = None
        self._mapping = {
            key.RIGHT: CharacterDirection.RIGHT,
            key.DOWN: CharacterDirection.DOWN,
            key.LEFT: CharacterDirection.LEFT,
            key.UP: CharacterDirection.UP,
        }
        self._move_vec = {
            CharacterDirection.RIGHT: Vec2(8, 0),
            CharacterDirection.DOWN: Vec2(0, -8),
            CharacterDirection.LEFT: Vec2(-8, 0),
            CharacterDirection.UP: Vec2(0, 8),
        }

    @property
    def batch(self) -> Batch:
        return self._char_sprite.batch

    @batch.setter
    def batch(self, batch: Batch):
        self._char_sprite.batch = batch
        self._bubble_sprite.batch = batch

    @property
    def group(self) -> Group:
        return self._char_sprite.group

    @group.setter
    def group(self, group: Group):
        self._group = Group(parent=group)
        self._char_sprite.group = self._group
        self._bubble_sprite.group = self._group

    @property
    def control_point(self) -> tuple[tuple[int, int]]:
        x, y = self.position
        pos0 = (x + 16, y + 4)  # left
        pos1 = (x + 32, y + 0)  # middle
        pos2 = (x + 48, y + 4)  # right
        pos3 = (x + 32, y + 20)  # up
        return pos0, pos1, pos2, pos3

    @property
    def room(self) -> "mystery.room.base.BaseRoom":
        return self._room

    @room.setter
    def room(self, room: "mystery.room.base.BaseRoom"):
        self._room = room

    @property
    def state(self) -> CharacterState:
        return self._state

    @state.setter
    def state(self, state: CharacterState):
        assert isinstance(state, CharacterState)
        self._state = state

    @property
    def direction(self) -> CharacterDirection:
        return self._direction

    @direction.setter
    def direction(self, direction: CharacterDirection):
        assert isinstance(direction, CharacterDirection)
        self._direction = direction

    @property
    def bubble(self) -> CharacterBubble:
        return self._bubble

    @bubble.setter
    def bubble(self, bubble: CharacterBubble):
        assert isinstance(bubble, CharacterBubble)
        self._bubble = bubble
        if bubble == CharacterBubble.EMPTY:
            self._bubble_sprite.visible = False
        else:
            self._bubble_sprite.image = bubble_anime[self._bubble]
            self._bubble_sprite.visible = True

    @property
    def position(self) -> tuple[int, int]:
        return self._char_sprite.position[:2]

    @position.setter
    def position(self, pos: tuple[int, int]):
        x, y, *_ = pos
        self._char_sprite.position = (x, y, 1)
        self._bubble_sprite.position = (x + 30, y + 50, 1)

    def _reset_bubble(self):
        self.bubble = CharacterBubble.EMPTY

    def update(self, dt: float):
        if self._state != CharacterState.FREEZE and (
            self._prev_state != self._state or self._prev_direction != self._direction
        ):
            state = self._prev_state = self._state.value
            direction = self._prev_direction = self._direction.value
            self._char_sprite.image = char_anime[state][direction]
        if self._state in (CharacterState.RUN, CharacterState.WALK):
            dx = self._move_vec[self._direction] / 8
            for _ in range(8):
                if self._state == CharacterState.RUN:
                    dp = dx * 2
                else:
                    dp = dx
                prev_pos = Vec2(*self.position)
                now_pos = prev_pos + dp
                if self._room and self._room.allow_move(now_pos[:]):
                    self.position = now_pos[:]
                else:
                    break

    def on_key_press(self, symbol, modifiers):
        if self._state == CharacterState.FREEZE:
            return
        elif symbol == key.LSHIFT:
            self._runnable = True
        elif key.LEFT <= symbol <= key.DOWN:
            self._direction = self._mapping[symbol]
            self._state = CharacterState.WALK
        if self._runnable and self._state == CharacterState.WALK:
            self._state = CharacterState.RUN

    def on_key_release(self, symbol, modifiers):
        if self._state == CharacterState.FREEZE:
            return
        if symbol == key.ESCAPE:
            self._game.window.switch_scene("menu")
        if symbol == key.SPACE:
            self._room.interact()
        elif symbol == key.LSHIFT:
            self._runnable = False
            if self._state == CharacterState.RUN:
                self._state = CharacterState.WALK
        elif key.LEFT <= symbol <= key.DOWN:
            if self._mapping[symbol] == self._direction:
                self._state = CharacterState.IDLE


__all__ = "CharacterState", "CharacterDirection", "CharacterBubble", "Character"
