# "Hook" file for PyInstaller to easily pack the game with
# assets and dynamic-imported modules.

from pathlib import Path

assets_path = Path(__file__).parent / "mystery" / "assets"
datas = [(assets_path, "assets")]

hiddenimports = [
    "mystery.rooms.start",
    "mystery.scenes.game",
    "mystery.scenes.settings",
    "mystery.scenes.settings.language",
    "mystery.scenes.settings.main",
    "mystery.scenes.start",
]
