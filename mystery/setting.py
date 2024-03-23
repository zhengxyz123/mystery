from collections import UserDict
from json import dump, load
from pathlib import Path


class Setting(UserDict):
    """Game setting."""

    def __init__(self, settings_path: Path):
        self._file = settings_path / "setting.json"
        if self._file.exists():
            self.data = load(open(self._file, "r", encoding="utf-8"))
            self._check_setting()
        else:
            self._init_setting()

    def _check_setting(self):
        if self.data.get("fps", 0) not in [30, 60, 90, 120]:
            self.data["fps"] = 60
        if self.data.get("skip_start_scene", False) not in [True, False]:
            self.data["skip_start_scene"] = False

    def _init_setting(self):
        self.data = {}
        self.data["fps"] = 60
        self.data["lang"] = "auto"
        self.data["skip_start_scene"] = False
        self.save()

    def save(self):
        dump(
            self.data,
            open(self._file, "w+", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )


__all__ = ("Setting",)
