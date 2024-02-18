from typing import Optional

from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.shapes import Circle
from pyglet.sprite import Sprite

from mystery.character import Character
from mystery.scenes import GameWindow
from mystery.tiled import TiledMap
from mystery.utils import point_in_polygon


class BaseRoom(EventDispatcher):
    """An example room, shows how rooms work."""

    def __init__(
        self,
        game: "mystery.scenes.game.GameScene",
        name: str,
        char: Character,
        group: Optional[Group] = None,
    ):
        self._game = game
        self._name = name
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

    def _allow_move(self, pos) -> bool:
        x, y = pos
        pos1 = (x + 20, y + 4)
        pos2 = (x + 44, y + 4)
        for poly in self._collisions_unwalkable.values():
            if point_in_polygon(poly, pos1) or point_in_polygon(poly, pos2):
                return False
        check1, check2 = [], []
        for poly in self._collisions_walkable:
            check1.append(point_in_polygon(poly, pos1))
            check2.append(point_in_polygon(poly, pos2))
        return any(check1) and any(check2)

    def _load_map(self):
        tmx_file = f"maps/{self._name}.tmx"
        map = TiledMap(tmx_file)
        for name, tiles in map.layers():
            parent, order = name.split("_")
            group = Group(int(order), self.parent_group[parent])
            self.child_group.append(group)
            for tile in tiles:
                sprite = Sprite(
                    tile.image,
                    tile.dest_x,
                    tile.dest_y,
                    batch=self.batch,
                    group=group,
                )
                self.sprits.append(sprite)
        for obj in map.objects("objects"):
            if obj.type == "CollisionPolygon":
                if obj.properties["can_walk"]:
                    self._collisions_walkable.append(obj.properties["points"])
                else:
                    self._collisions_unwalkable.setdefault(
                        obj.properties["cp_name"], obj.properties["points"]
                    )
            elif obj.type == "SpawnPoint":
                name = obj.properties["sp_name"]
                position = (obj.x, obj.y)
                self._spawn_points[name] = position
        self.char.position = self._spawn_points["start"]

    def draw(self):
        char_pos = Vec3(*self.char.position, 0)
        center_pos = Vec3(
            self._game.window.width // 2 - 32, self._game.window.height // 2 - 32, 0
        )
        trans_mat = Mat4.from_translation(center_pos - char_pos)
        with self._game.window.apply_view(trans_mat):
            self.batch.draw()

    def on_room_enter(self, *args):
        self._load_map()

    def on_rome_leave(self, *args):
        pass


BaseRoom.register_event_type("on_room_enter")
BaseRoom.register_event_type("on_room_leave")


__all__ = ("BaseRoom",)
