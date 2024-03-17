from typing import Optional

from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.sprite import Sprite
from pytmx import TiledTileLayer

from mystery.character import Character
from mystery.utils import Rect


class BaseRoom(EventDispatcher):
    """The base class of a room.

    A room is a place for player to interact with the game map.
    """

    def __init__(
        self,
        game: "mystery.scenes.game.GameScene",
        name: str,
        char: Character,
        group: Optional[Group] = None,
    ):
        self._game = game
        self._name = name
        self._map_loaded = False
        self.char = char
        self.batch = Batch()
        self.parent_group = {
            "back": Group(order=1, parent=group),
            "char": Group(order=2, parent=group),
            "fore": Group(order=3, parent=group),
        }
        self.child_group = []
        self.char.batch = self.batch
        self.char.group = self.parent_group["char"]
        self.char.room = self
        self.sprits = []

        # One is a list, the other is a dict.
        self._collisions_walkable = []
        self._collisions_unwalkable = {}
        self._spawn_points = {}

    @property
    def name(self) -> str:
        return self._name

    def allow_move(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        pos1 = (x + 20, y + 4)
        pos2 = (x + 44, y + 4)
        for rect in self._collisions_unwalkable.values():
            if pos1 in rect or pos2 in rect:
                return False
        check1, check2 = [], []
        for rect in self._collisions_walkable:
            check1.append(pos1 in rect)
            check2.append(pos2 in rect)
        return any(check1) and any(check2)

    def _load_map(self):
        if self._map_loaded:
            return
        map = self._game.window.resource.map(self._name)
        tw, th = map.tilewidth, map.tileheight
        for layer in map.layers:
            if not isinstance(layer, TiledTileLayer):
                continue
            parent, order = layer.name.split("_")
            group = Group(int(order), self.parent_group[parent])
            self.child_group.append(group)
            h = layer.height - 1
            for tile in layer.tiles():
                x, y, image = tile
                sprite = Sprite(
                    image, x * tw, (h - y) * th, batch=self.batch, group=group
                )
                self.sprits.append(sprite)
        for obj in map.objects:
            obj.y = (map.tileheight * map.height) - obj.y - obj.height
            if obj.type == "CRect":
                if obj.properties["can_walk"]:
                    self._collisions_walkable.append(Rect.from_tmx_obj(obj))
                else:
                    name = obj.properties["cr_name"]
                    self._collisions_unwalkable[name] = Rect.from_tmx_obj(obj)
            elif obj.type == "SPoint":
                name = obj.properties["sp_name"]
                self._spawn_points[name] = (obj.x, obj.y)
        self._map_loaded = True

    def draw(self):
        char_pos = Vec3(*self.char.position, 0)
        center_pos = Vec3(
            self._game.window.width // 2 - 32, self._game.window.height // 2 - 32, 0
        )
        trans_mat = Mat4.from_translation(center_pos - char_pos)
        with self._game.window.apply_view(trans_mat):
            self.batch.draw()

    def on_room_enter(self, *args):
        pass

    def on_rome_leave(self, *args):
        pass


BaseRoom.register_event_type("on_room_enter")
BaseRoom.register_event_type("on_room_leave")


__all__ = ("BaseRoom",)
