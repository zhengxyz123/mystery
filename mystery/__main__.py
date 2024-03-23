import sys
from json import dump
from time import strftime
from traceback import format_exc, print_exc

from pyglet import app, clock, gl
from pyglet.image import Texture

from mystery import data_path, game_setting, version
from mystery.scenes import GameWindow
from mystery.scenes.menu import MenuScene


def record_error():
    print_exc()
    with open(data_path / "log" / strftime("error_%Y%m%d_%H%M%S.json"), "w+") as f:
        dump(
            {
                "traceback": format_exc().splitlines(),
                "platform": sys.platform,
                "pythonVersion": "{}.{}.{}".format(*sys.version_info),
                "gameVersion": version,
                "frozen": getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"),
            },
            f,
            ensure_ascii=False,
            indent=4,
        )


def start():
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    Texture.default_min_filter = gl.GL_NEAREST
    Texture.default_mag_filter = gl.GL_NEAREST
    try:
        window = GameWindow(768, 576, resizable=True)
        window.add_scene("menu", MenuScene)
        window.switch_scene("menu")
        clock.schedule_interval(window.draw, 1 / game_setting["fps"])
        app.run()
    except:
        record_error()
        exit(1)


if __name__ == "__main__":
    start()
