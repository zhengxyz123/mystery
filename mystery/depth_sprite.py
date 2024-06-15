# A submodule came from pyglet's example: examples/sprite/depth_sprites.py

from pyglet import gl, sprite
from pyglet.graphics.shader import Shader, ShaderProgram

fragment_source = """
    #version 150 core
    in vec4 vertex_colors;
    in vec3 texture_coords;
    out vec4 final_colors;

    uniform sampler2D sprite_texture;

    void main() {
        final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;
        if (final_colors.a < 0.01) {
            discard;
        }
    }
"""

vertex_shader = Shader(sprite.vertex_source, "vertex")
fragment_shader = Shader(fragment_source, "fragment")
depth_shader = ShaderProgram(vertex_shader, fragment_shader)


class DepthSpriteGroup(sprite.SpriteGroup):
    def set_state(self):
        self.program.use()
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(self.texture.target, self.texture.id)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(self.blend_src, self.blend_dest)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

    def unset_state(self):
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.program.stop()


class DepthSprite(sprite.AdvancedSprite):
    group_class = DepthSpriteGroup

    def __init__(
        self,
        img,
        x=0,
        y=0,
        z=0,
        blend_src=gl.GL_SRC_ALPHA,
        blend_dest=gl.GL_ONE_MINUS_SRC_ALPHA,
        batch=None,
        group=None,
        subpixel=False,
        program=None,
    ):
        program = depth_shader
        super().__init__(
            img, x, y, z, blend_src, blend_dest, batch, group, subpixel, program
        )


__all__ = ("DepthSprite", "DepthSpriteGroup")
