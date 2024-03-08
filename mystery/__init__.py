from locale import getdefaultlocale
from pathlib import Path

from pyglet import version as pyglet_ver
from pyglet.resource import get_data_path, get_settings_path

from mystery.resource import ResourceManager
from mystery.setting import Setting

version = "0.0.1"

# Check version of dependencies.
if pyglet_ver != "2.0.14":
    print(f"This game must use pyglet 2.0.14, but {pyglet_ver} found.")
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
setting = Setting(settings_path)

resmgr = ResourceManager()
if setting["lang"] == "auto":
    lang_code = getdefaultlocale()[0].lower()
else:
    lang_code = setting.get("lang", "en_us")
resmgr.language = lang_code

__all__ = "version", "data_path", "setting", "resmgr"
