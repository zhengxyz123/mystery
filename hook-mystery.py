# "Hook" file for PyInstaller to easily pack the game with
# assets and dynamic-imported modules.

datas = [("mystery/assets", "assets")]

hiddenimports = [
    "mystery.rooms.start",
    "mystery.scenes.game",
    "mystery.scenes.settings",
    "mystery.scenes.settings.language",
    "mystery.scenes.settings.main",
    "mystery.scenes.start",
]
