from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.shapes import Circle
from pyglet.sprite import Sprite

from mystery import resmgr
from mystery.character import Character
from mystery.scenes import GameWindow
from mystery.tiled import TiledMap
from mystery.utils import point_in_polygon


class BaseRoom(EventDispatcher):
    def __init__(
        self,
        window: GameWindow,
        game: "mystery.scenes.game.GameScene",
        char: Character,
    ):
        self._window = window
        self._game = game
        self.char = char
        self.batch = Batch()
        self.base_group = {
            "back": Group(order=0),
            "char": Group(order=1),
            "fore": Group(order=2),
        }
        self.char.batch = self.batch
        self.char.group = self.base_group["char"]
        self.char.room = self
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
        pos1 = pos[0] + 20, pos[1] + 3
        pos2 = pos1[0] + 24, pos1[1]
        check1, check2 = [], []
        for poly in self._collisions:
            check1.append(point_in_polygon(poly, pos1))
            check2.append(point_in_polygon(poly, pos2))
        return any(check1) and any(check2)

    def _load_map(self):
        tmx_file = f"maps/{self._name}.tmx"
        map = TiledMap(tmx_file)
        for name, tiles in map.layers():
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
        for objs in map.objects():
            if objs.type == "CollisionPolygon":
                self._collisions.append(objs.properties["points"])
            elif objs.type == "SpawnPoint":
                name = objs.properties["sp_name"]
                position = (objs.x, objs.y)
                self._spawn_points[name] = position
        self.char.position = self._spawn_points["start"]

    def draw(self):
        char_pos = Vec3(*self.char.position, 0)
        center_pos = Vec3(
            self._window.width // 2 - 32, self._window.height // 2 - 32, 0
        )
        trans_mat = Mat4.from_translation(center_pos - char_pos)
        with self._window.apply_view(trans_mat):
            self.batch.draw()

    def on_room_enter(self, *args):
        pass

    def on_rome_leave(self, *args):
        pass


BaseRoom.register_event_type("on_room_enter")
BaseRoom.register_event_type("on_room_leave")


__all__ = "BaseRoom"
