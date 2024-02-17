from base64 import b64decode
from collections import namedtuple
from collections.abc import Iterator
from gzip import decompress as gzip_decompress
from struct import unpack
from xml.etree import ElementTree
from zlib import decompress as zlib_decompress

from mystery import resmgr

MapInfo = namedtuple("MapInfo", "version orientation render_order")
Tile = namedtuple("Tile", "image dest_x dest_y collision")
Object = namedtuple("Object", "name x y width height type arg properties")
Layer = namedtuple("Layer", "name gids")
SourceTile = namedtuple("SourceTile", "img_name img_size source_x source_y collision")


class TiledMap:
    def __init__(self, tmx_file: str, invert_y: bool = True):
        self._root = ElementTree.parse(resmgr.loader.file(tmx_file, "r")).getroot()
        self._invert_y = invert_y
        self._size = None
        self._bgcolor_converted = None
        self._version = self._root.get("tiledversion", "0.0")
        self._orientation = self._root.get("orientation", "orthogonal")
        self._render_order = self._root.get("renderorder", "right-down")
        self._bgcolor = self._root.get("backgroundcolor", "#000000")
        self._infinite = int(self._root.get("infinite", 0))
        assert (
            self._orientation == "orthogonal"
        ), "Only orthogonal orientation is supported"
        assert (
            self._render_order == "right-down"
        ), "Only right-down render order is supported"

    @property
    def info(self) -> MapInfo:
        return MapInfo(self._version, self._orientation, self._render_order)

    @property
    def bgcolor(self) -> tuple[int, ...]:
        if self._bgcolor_converted is not None:
            return self._bgcolor_converted
        color = int(self._bgcolor[1:], base=16)
        b = color & 0xFF
        color = (color - b) >> 8
        g = color & 0xFF
        color = (color - g) >> 8
        r = color & 0xFF
        color = (color - r) >> 8
        a = color if color > 0 else 255
        self._bgcolor_converted = (r, g, b, a)
        return self._bgcolor_converted

    @property
    def size(self) -> tuple[int, int]:
        if self._infinite == 1:
            return (-1, -1)
        if self._size is not None:
            return self._size
        tile_width = int(self._root.get("tilewidth"))
        tile_height = int(self._root.get("tileheight"))
        map_width = int(self._root.get("width")) * tile_width
        map_height = int(self._root.get("height")) * tile_height
        self._size = (map_width, map_height)
        return self._size

    def _decode_tilesets(self) -> dict[int, SourceTile]:
        all_tilesets = self._root.findall("tileset")
        tilesets = {}
        for tileset in all_tilesets:
            first_gid = int(tileset.get("firstgid"))
            source_name = tileset.get("source")
            source_file = resmgr.loader.file(f"maps/{source_name}", "r")
            source = ElementTree.parse(source_file).getroot()
            columns = int(source.get("columns"))
            tile_width = int(source.get("tilewidth"))
            tile_height = int(source.get("tileheight"))
            tile_count = int(source.get("tilecount"))
            image = source.find("image")
            image_filename = image.get("source")
            image_size = int(image.get("width")), int(image.get("height"))
            tile_properties = {}
            for tile in source.findall("tile"):
                tile_id = int(tile.get("id"))
                for objgroup in tile:
                    for obj in objgroup:
                        x, y, w, h = (
                            int(obj.get("x")),
                            int(obj.get("y")),
                            int(obj.get("width")),
                            int(obj.get("height")),
                        )
                        if self._invert_y:
                            y = tile_height - h
                        tile_properties[tile_id] = (x, y, w, h)
            for i in range(tile_count):
                column = i % columns
                row = (i % tile_count - column) // columns
                x = column * tile_width
                y = row * tile_height
                gid = i + first_gid
                collision = tile_properties.get(i, None)
                tilesets[gid] = SourceTile(image_filename, image_size, x, y, collision)
        return tilesets

    def _get_map_gid_dests(self) -> dict[int, tuple[int, int]]:
        """Get mapping of [gid] to (x, y) target destinations."""
        tile_width = int(self._root.get("tilewidth"))
        tile_height = int(self._root.get("tileheight"))
        image_width = int(self._root.get("width")) * tile_width
        image_height = int(self._root.get("height")) * tile_height
        map_columns = image_width // tile_width
        map_rows = image_height // tile_height
        tile_count = map_columns * map_rows
        gid_loc = {}
        for i in range(tile_count):
            column = i % map_columns
            row = (i % tile_count - column) // map_columns
            x = column * tile_width
            y = row * tile_height
            gid_loc[i] = (x, y)
        return gid_loc

    def _decode_layer(self, layer: ElementTree.Element) -> Layer:
        layer_name = layer.get("name")
        data_element = layer.find("data")
        encoding = data_element.get("encoding")
        compression = data_element.get("compression")
        if encoding == "base64":
            data = b64decode(data_element.text.strip())
            if compression == "zlib":
                data = zlib_decompress(data)
            elif compression == "gzip":
                data = gzip_decompress(data)
            else:
                raise NotImplementedError(
                    f"compression '{compression}' not yet supported"
                )
            gid_tuples = [unpack("<I", data[i : i + 4]) for i in range(0, len(data), 4)]
            gid_list = [g[0] for g in gid_tuples]
        elif encoding == "csv":
            gid_list = [int(g) for g in data_element.text.replace("\n", "").split(",")]
        else:
            raise NotImplementedError(f"encoding '{encoding}' not yet supported")
        return Layer(layer_name, gid_list)

    def _map_copy_rects(self, layer: ElementTree.Element) -> Iterator[tuple]:
        tileset_dict = self._decode_tilesets()
        map_gid_dests = self._get_map_gid_dests()
        layerobj = self._decode_layer(layer)
        for i, gid in enumerate(layerobj.gids):
            if not gid:
                continue
            src_tile = tileset_dict[gid]
            source_x, source_y = src_tile.source_x, src_tile.source_y
            dest_x, dest_y = map_gid_dests[i]
            yield (
                src_tile.img_name,
                src_tile.img_size,
                source_x,
                source_y,
                dest_x,
                dest_y,
                src_tile.collision,
            )

    def layers(self) -> Iterator[tuple[str, Tile]]:
        tile_width = int(self._root.get("tilewidth"))
        tile_height = int(self._root.get("tileheight"))
        map_height = int(self._root.get("height")) * tile_height
        all_layers = self._root.findall(".//layer")
        for layer in all_layers:
            name = layer.get("name")
            tiles = []
            for (
                img,
                size,
                src_x,
                src_y,
                dst_x,
                dst_y,
                collision,
            ) in self._map_copy_rects(layer):
                img_width, img_height = size
                if self._invert_y:
                    dst_y = map_height - tile_height - dst_y
                    src_y = img_height - tile_height - src_y
                source = resmgr.loader.image(f"maps/tilesets/{img}")
                image = source.get_region(src_x, src_y, tile_width, tile_height)
                tile = Tile(image, dst_x, dst_y, collision)
                tiles.append(tile)
            yield name, tiles

    def objects(self, layer_name: str) -> Iterator[Object]:
        tile_height = int(self._root.get("tileheight"))
        map_height = int(self._root.get("height")) * tile_height
        for object_group in self._root.findall("objectgroup"):
            if object_group.get("name") != layer_name:
                continue
            for obj in object_group:
                oname = str(obj.get("name", ""))
                otype = str(obj.get("type", ""))
                x = float(obj.get("x"))
                y = float(obj.get("y"))
                width = float(obj.get("width", 0.0))
                height = float(obj.get("height", 0.0))
                arg = str(obj.get("arg", ""))
                if self._invert_y:
                    y = map_height - height - y
                properties = {}
                for obj_properties in obj:
                    if (
                        points := obj_properties.get("points")
                    ) and obj_properties.tag == "polygon":
                        converted = []
                        for n in points.split(" "):
                            dx, dy = (float(i) for i in n.split(","))
                            converted.append((x + dx, y - dy))
                        properties["points"] = converted
                    for prop in obj_properties:
                        pname = prop.get("name")
                        ptype = prop.get("type")
                        pvalue = prop.get("value")
                        if ptype == "int":
                            pvalue = int(pvalue)
                        elif ptype == "float":
                            pvalue = float(pvalue)
                        elif ptype == "bool":
                            assert pvalue in ["true", "false"]
                            pvalue = pvalue == "true"
                        properties[pname] = pvalue
                yield Object(oname, x, y, width, height, otype, arg, properties)


__all__ = ("TiledMap",)
