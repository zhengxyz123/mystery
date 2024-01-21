from pyglet import app, clock, gl
from pyglet.image import Texture

from mystery import setting
from mystery.scenes import GameWindow
from mystery.scenes.menu import MenuScene


def start():
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    Texture.default_min_filter = gl.GL_NEAREST
    Texture.default_mag_filter = gl.GL_NEAREST

    window = GameWindow(768, 576, resizable=True)
    window.add_scene("menu", MenuScene)
    window.switch_scene("menu")
    clock.schedule_interval(window.draw, 1 / setting["fps"])
    app.run()


if __name__ == "__main__":
    start()
