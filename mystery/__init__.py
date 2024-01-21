from locale import getdefaultlocale
from pathlib import Path

from pyglet import version as pyglet_ver
from pyglet.resource import get_data_path, get_settings_path

from mystery.resource import ResourceManager
from mystery.setting import Setting

version = "0.0.1"
data_path = Path(get_data_path("mystery"))
settings_path = Path(get_settings_path("mystery"))

# Check pyglet version.
if pyglet_ver != "2.0.10":
    print(f"This game must use pyglet 2.0.10, but {pyglet_ver} found.")
    exit(1)

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

resource = ResourceManager()
if setting["lang"] == "auto":
    lang_code = getdefaultlocale()[0].lower()
else:
    lang_code = setting.get("lang", "en_us")
resource.language = lang_code

__all__ = "version", "data_path", "setting", "resource"
