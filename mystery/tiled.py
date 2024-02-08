import os
from base64 import b64decode
from collections import namedtuple
from functools import cache
from gzip import decompress as gzip_decompress
from struct import unpack
from xml.etree import ElementTree
from zlib import decompress as zlib_decompress

from mystery import resmgr

Tile = namedtuple(
    "Tile", "source width height source_x source_y dest_x dest_y collision"
)
Object = namedtuple("Object", "name x y width height type arg properties")
ObjectProperty = namedtuple("ObjectProperty", "name type value")
Layer = namedtuple("Layer", "name gids")
SourceTile = namedtuple("SourceTile", "img_name img_size source_x source_y collision")


@cache
def _get_map_root(tmx_filename):
    tmx_file = resmgr.loader.file(f"maps/{tmx_filename}", "r")
    map_root = ElementTree.parse(tmx_file).getroot()
    version = map_root.get("tiledversion")
    orientation = map_root.get("orientation")
    render_order = map_root.get("renderorder")
    assert render_order == "right-down", "Only right-down render order is supported"
    assert orientation == "orthogonal", "Only orthogonal orientation is supported"
    return map_root


def _decode_layer(layer):
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
        gid_tuples = [unpack("<I", data[i : i + 4]) for i in range(0, len(data), 4)]
        gid_list = [g[0] for g in gid_tuples]
    elif encoding == "csv":
        gid_list = [int(g) for g in data_element.text.replace("\n", "").split(",")]
    else:
        raise NotImplementedError(f"'{encoding}' encoding not yet supported")
    return Layer(layer_name, gid_list)


@cache
def _decode_tilesets(map_root, flip_y):
    # TODO: support spacing and margin
    all_tilesets = map_root.findall("tileset")
    tilesets_dict = {}
    for tileset in all_tilesets:
        first_gid = int(tileset.get("firstgid"))
        source_name = tileset.get("source")
        source_file = resmgr.loader.file(f"maps/{source_name}", "r")
        source = ElementTree.parse(source_file).getroot()
        # tileset_name = source.get("name")
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
                    # These are RELATIVE coordinates:
                    x, y, w, h = (
                        int(obj.get("x")),
                        int(obj.get("y")),
                        int(obj.get("width")),
                        int(obj.get("height")),
                    )
                    if flip_y:
                        y = tile_height - h
                    tile_properties[tile_id] = (x, y, w, h)
        for i in range(tile_count):
            column = i % columns
            row = (i % tile_count - column) // columns
            x = column * tile_width
            y = row * tile_height
            gid = i + first_gid
            collision = tile_properties.get(i, None)
            tilesets_dict[gid] = SourceTile(image_filename, image_size, x, y, collision)
    return tilesets_dict


@cache
def _get_map_gid_destinations(map_root):
    """Get mapping of [gid] to (x, y) target destinations."""
    # TODO: support different render orders, besides right-down.
    tile_width = int(map_root.get("tilewidth"))
    tile_height = int(map_root.get("tileheight"))
    image_width = int(map_root.get("width")) * tile_width
    image_height = int(map_root.get("height")) * tile_height
    map_columns = image_width // tile_width
    map_rows = image_height // tile_height
    tile_count = map_columns * map_rows
    gid_location_dict = dict()
    for i in range(tile_count):
        column = i % map_columns
        row = (i % tile_count - column) // map_columns
        x = column * tile_width
        y = row * tile_height
        gid_location_dict[i] = (x, y)
    return gid_location_dict


def _map_copy_rects(map_root, layer, flip_y):
    tileset_dict = _decode_tilesets(map_root, flip_y)
    map_gid_destinations = _get_map_gid_destinations(map_root)
    layerobj = _decode_layer(layer)
    for i, gid in enumerate(layerobj.gids):
        if not gid:
            continue
        # Get source tile by gid:
        src_tile = tileset_dict[gid]
        source_x, source_y = src_tile.source_x, src_tile.source_y
        # Get destination by final map index:
        dest_x, dest_y = map_gid_destinations[i]
        yield src_tile.img_name, src_tile.img_size, source_x, source_y, dest_x, dest_y, src_tile.collision


# Public functions:


def get_map_size(tmx_filename):
    map_root = _get_map_root(tmx_filename)
    tile_width = int(map_root.get("tilewidth"))
    tile_height = int(map_root.get("tileheight"))
    map_width = int(map_root.get("width")) * tile_width
    map_height = int(map_root.get("height")) * tile_height
    return map_width, map_height


def get_tile_layers(tmx_filename, flip_y=True):
    map_root = _get_map_root(tmx_filename)
    tile_width = int(map_root.get("tilewidth"))
    tile_height = int(map_root.get("tileheight"))
    map_height = int(map_root.get("height")) * tile_height
    all_layers = map_root.findall("layer")
    layer_tiles = {}
    for layer in all_layers:
        name = layer.get("name")
        tiles = []
        for img, size, src_x, src_y, dst_x, dst_y, collision in _map_copy_rects(
            map_root, layer, flip_y
        ):
            img_width, img_height = size
            # Flip y render order for pyglet:
            if flip_y:
                dst_y = map_height - tile_height - dst_y
                src_y = img_height - tile_height - src_y
            source = resmgr.loader.image(f"maps/tilesets/{img}")
            tile = Tile(
                source, tile_width, tile_height, src_x, src_y, dst_x, dst_y, collision
            )
            tiles.append(tile)
        layer_tiles.setdefault(name, tiles)
    return layer_tiles


def get_object_layer(tmx_filename, layer_name, flip_y=True):
    map_root = _get_map_root(tmx_filename)
    tile_height = int(map_root.get("tileheight"))
    map_height = int(map_root.get("height")) * tile_height
    for object_group in map_root.findall("objectgroup"):
        # Skip layers with other names:
        if object_group.get("name") != layer_name:
            continue
        for obj in object_group:
            # Base object attributes:
            oname = str(obj.get("name", ""))
            otype = str(obj.get("type", ""))  # AKA 'Class'
            x = float(obj.get("x"))
            y = float(obj.get("y"))
            width = float(obj.get("width", 0.0))
            height = float(obj.get("height", 0.0))
            arg = str(obj.get("arg", ""))
            if flip_y:
                y = map_height - height - y
            properties = []
            # Optional properties:
            for obj_properties in obj:
                if points := obj_properties.get("points"):
                    converted = []
                    for n in points.split(" "):
                        dx, dy = (float(i) for i in n.split(","))
                        converted.append((x + dx, y - dy))
                    properties.append(ObjectProperty("points", None, converted))
                for prop in obj_properties:
                    pname = prop.get("name")
                    ptype = prop.get("type")
                    pvalue = prop.get("value")
                    properties.append(ObjectProperty(pname, ptype, pvalue))
            yield Object(oname, x, y, width, height, otype, arg, properties)


__all__ = "get_map_size", "get_tile_layers", "get_object_layer"
