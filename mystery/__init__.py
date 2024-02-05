from locale import getdefaultlocale
from logging import CRITICAL, getLogger
from pathlib import Path

# Disable logger of pytmx.utils_pygame because we never use pygame.
pytmx_logger = getLogger("pytmx.util_pygame")
pytmx_logger.setLevel(CRITICAL + 1)

from pyglet import version as pyglet_ver
from pyglet.resource import get_data_path, get_settings_path
from pytmx import __version__ as pytmx_ver

from mystery.resource import ResourceManager
from mystery.setting import Setting

version = "0.0.1"

# Check version of dependencies.
if pyglet_ver != "2.0.10":
    print(f"This game must use pyglet 2.0.10, but {pyglet_ver} found.")
    exit(1)
if pytmx_ver != (3, 32):
    ver = f"{pytmx_ver[0]}.{pytmx_ver[1]}"
    print(f"This game must use pytmx 3.32, but {ver} found.")
    exit(1)

data_path = Path(get_data_path("mystery"))
settings_path = Path(get_settings_path("mystery"))
# Create data path.
if not data_path.exists():
    data_path.mkdir()
for subpath in ["screenshots", "saves"]:
    if not (p := data_path / subpath).exists():
        p.mkdir()
# Create settings path.
if not settings_path.exists():
    settings_path.mkdir()
setting = Setting(settings_path)

resmgr = ResourceManager()
if setting["lang"] == "auto":
    lang_code = getdefaultlocale()[0].lower()
else:
    lang_code = setting.get("lang", "en_us")
resmgr.language = lang_code

__all__ = "version", "data_path", "setting", "resmgr"
