from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.sprite import Sprite
from pyglet.window import Window

from mystery import resmgr
from mystery.character import Character
from mystery.tiled import get_object_layer, get_tile_layers
from mystery.utils import point_in_polygon


class BaseRoom(EventDispatcher):
    def __init__(
        self,
        window: Window,
        char: Character,
    ):
        self._window = window
        self.char = char
        self.batch = Batch()
        self.base_group = {
            "back": Group(order=0),
            "char": Group(order=1),
            "fore": Group(order=2),
        }
        self.char.batch = self.batch
        self.char.group = self.base_group["char"]
        self.char.allow_move = self._allow_move
        self.other_groups = []
        self.sprits = []

        self._name = "example"
        self._collisions = []
        self._spawn_points = {}
        self._load_map()

    @property
    def name(self) -> str:
        return self._name

    def _allow_move(self, pos) -> bool:
        for poly in self._collisions:
            pos1 = pos[0] + 15, pos[1]
            pos2 = pos1[0] + 34, pos1[1]
            if not (point_in_polygon(poly, pos1) and point_in_polygon(poly, pos2)):
                return False
        return True

    def _load_map(self):
        tmx_file = self._name + ".tmx"
        for name, tiles in get_tile_layers(tmx_file).items():
            parent, order = name.split("_")
            group = Group(int(order), self.base_group[parent])
            self.other_groups.append(group)
            for tile in tiles:
                image = tile.source.get_region(
                    tile.source_x, tile.source_y, tile.width, tile.height
                )
                sprite = Sprite(
                    image,
                    tile.dest_x,
                    tile.dest_y,
                    batch=self.batch,
                    group=group,
                )
                self.sprits.append(sprite)
        for objs in get_object_layer(tmx_file, "objects"):
            if objs.type == "CollisionPolygon":
                self._collisions.append(objs.properties[0].value)
            elif objs.type == "SpawnPoint":
                name = objs.properties[0].value
                position = (objs.x, objs.y)
                self._spawn_points[name] = position
        self.char.position = self._spawn_points["start"]

    def draw(self):
        char_pos = Vec3(*self.char.position, 0)
        center_pos = Vec3(self._window.width // 2 - 32, self._window.height // 2 - 32, 1)
        trans_mat = Mat4.from_translation(center_pos - char_pos)
        with self._window.apply_view(trans_mat):
            self.batch.draw()


__all__ = "BaseRoom"
