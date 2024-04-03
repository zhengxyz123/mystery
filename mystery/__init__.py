from locale import getdefaultlocale
from logging import getLogger
from pathlib import Path

# Disable pytmx's logger.
getLogger("pytmx").setLevel(999)

from pyglet import version as pyglet_ver
from pyglet.resource import get_data_path, get_settings_path
from pytmx import __version__ as pytmx_ver

from mystery.resource import ResourceManager
from mystery.setting import Setting

version = "0.0.1"

# Check version of dependencies.
if pyglet_ver != "2.0.15":
    print(f"This game must use pyglet 2.0.15, but {pyglet_ver} found.")
    exit(1)
if pytmx_ver != (3, 32):
    print("This game must use pytmx 3.32, but {}.{} found.".format(*pytmx_ver))
    exit(1)

data_path = Path(get_data_path("mystery"))
settings_path = Path(get_settings_path("mystery"))
# Create data path.
if not data_path.exists():
    data_path.mkdir()
for subpath in ["log", "saves", "screenshots"]:
    if not (p := data_path / subpath).exists():
        p.mkdir()
# Create settings path.
if not settings_path.exists():
    settings_path.mkdir()
game_setting = Setting(settings_path)

resmgr = ResourceManager()
if game_setting["lang"] == "auto":
    lang_code = getdefaultlocale()[0].lower()
else:
    lang_code = game_setting.get("lang", "en_us")
resmgr.language = lang_code

__all__ = "version", "data_path", "setting", "resmgr"
