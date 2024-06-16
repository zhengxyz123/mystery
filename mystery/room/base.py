from typing import Optional

from pyglet import gl
from pyglet.event import EventDispatcher
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.sprite import Sprite
from pytmx import TiledTileLayer

from mystery.character import Character, CharacterDirection
from mystery.depth_sprite import DepthSprite
from mystery.scene.game import GameScene
from mystery.utils import Rect


class BaseRoom(EventDispatcher):
    """The base class of a room.

    A room is a place for player to interact with the game map.
    """

    def __init__(
        self,
        game: GameScene,
        map_name: str,
        character: Character,
        group: Optional[Group] = None,
    ):
        self.game = game
        self.map_name = map_name
        self.tiled_map = self.game.window.resource.tiled_map(self.map_name)
        self._map_loaded = False
        self.map_batches = {
            "back": Batch(),
            "char": Batch(),
            "fore": Batch(),
        }
        self.gui_batch = Batch()
        self.sprite_groups = []
        self.sprites_list = []
        self.ibojs_dict = {}

        self.character = character
        self.character.batch = self.map_batches["char"]
        self.character.room = self

        self._collisions_walkable = []
        self._collisions_unwalkable = {}
        self._spawn_points = {}

        # A dict that store the room info.
        # It must be capable of turning into JSON!
        self.data = {}

    @property
    def name(self) -> str:
        return self.map_name

    def _load_map(self):
        if self._map_loaded:
            return
        tw, th = self.tiled_map.tilewidth, self.tiled_map.tileheight
        for layer in self.tiled_map.layers:
            if not isinstance(layer, TiledTileLayer):
                continue
            batch_name, group_order = layer.name.split("_")
            group = Group(int(group_order))
            self.sprite_groups.append(group)
            h = layer.height - 1
            for tile in layer.tiles():
                x, y, image = tile
                sprite = Sprite(
                    image,
                    x * tw,
                    (h - y) * th,
                    batch=self.map_batches[batch_name],
                    group=group,
                )
                self.sprites_list.append(sprite)
        for obj in self.tiled_map.objects:
            obj.y = (
                (self.tiled_map.tileheight * self.tiled_map.height) - obj.y - obj.height
            )
            if obj.type == "CRect":
                if obj.properties["can_walk"]:
                    self._collisions_walkable.append(Rect.from_tmx_obj(obj))
                else:
                    name = obj.properties["cr_name"]
                    self._collisions_unwalkable[name] = Rect.from_tmx_obj(obj)
            elif obj.type == "IObj":
                image = self.tiled_map.get_tile_image_by_gid(obj.gid)
                iobj_name = obj.name
                sprite = DepthSprite(
                    image, obj.x, obj.y, batch=self.map_batches["char"]
                )
                self.ibojs_dict[iobj_name] = sprite
            elif obj.type == "SPoint":
                name = obj.properties["sp_name"]
                self._spawn_points[name] = (obj.x, obj.y)
        self._map_loaded = True

    def _update_iobjs(self):
        char_y = self.character.position[1] + 4
        for iobj in self.ibojs_dict.values():
            if iobj.y > char_y:
                iobj.z = 0
            else:
                iobj.z = 2

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
        if any(check1) and any(check2):
            self._update_iobjs()
            return True
        else:
            return False

    def check_collide(self, which: str) -> bool:
        """Check whether a character can intercat with a collision box.

        `which` is a key in `BaseRoom._collisions_unwalkable`.
        """
        char_dir = self.character.direction
        points = self.character.control_point
        rect = self._collisions_unwalkable[which]
        t = tuple((point in rect for point in points))
        if t == (True, False, False, False):
            return char_dir == CharacterDirection.LEFT
        elif t == (False, False, True, False):
            return char_dir == CharacterDirection.RIGHT
        elif t == (False, False, False, True):
            return char_dir == CharacterDirection.UP
        elif t[1] and not t[3]:
            return char_dir == CharacterDirection.DOWN
        else:
            return False

    def draw(self):
        char_pos = Vec3(*self.character.position, 0)
        center_pos = Vec3(
            self.game.window.width // 2 - 32, self.game.window.height // 2 - 32, 0
        )
        trans_mat = Mat4.from_translation(center_pos - char_pos)
        with self.game.window.apply_view(trans_mat):
            self.map_batches["back"].draw()
            self.map_batches["char"].draw()
            self.map_batches["fore"].draw()
        self.gui_batch.draw()

    def interact(self):
        pass

    def on_room_enter(self, *args):
        pass

    def on_rome_leave(self):
        pass


BaseRoom.register_event_type("on_room_enter")
BaseRoom.register_event_type("on_room_leave")


__all__ = ("BaseRoom",)
