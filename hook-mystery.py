# "Hook" file for PyInstaller to easily pack the game with
# assets and dynamic-imported modules.

from pathlib import Path

assets_path = Path(__file__).parent / "mystery" / "assets"
datas = [(assets_path, "assets")]

hiddenimports = [
    "mystery.room.start",
    "mystery.scene.game",
    "mystery.scene.settings",
    "mystery.scene.settings.language",
    "mystery.scene.settings.main",
    "mystery.scene.start",
]
