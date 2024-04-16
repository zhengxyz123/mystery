#!/usr/bin/env python3

import argparse
import os
import platform
import shutil
import subprocess
import sys
import zipapp
from pathlib import Path
from textwrap import dedent

parser = argparse.ArgumentParser(
    prog="build.py",
    description="mystery release file builder",
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=True,
    allow_abbrev=True,
)
parser.add_argument(
    "type",
    help=dedent(
        """\
        what kind of file to build:
        - exec: create executable file using PyInstaller
        - pyz: generate zip archive using zipapp
        """
    ),
    choices=["exec", "pyz"],
    metavar="type",
)
parser.add_argument(
    "-c",
    "--compressed",
    action="store_true",
    help="compress pyz file",
)
parser.add_argument(
    "-p",
    "--pack",
    action="store_true",
    help="pack executable files into a zip file",
)


def get_version():
    mystery_src = Path(__file__).parent / "mystery"
    with (mystery_src / "__init__.py").open("r") as f:
        for line in f.readlines():
            if line.startswith("version = "):
                start = line.find('"')
                end = line.find('"', start + 1)
                return line[start + 1 : end]
    return "0.0.0"


def check():
    build_py_path = Path(__file__).parent
    if not (build_py_path / "mystery" / "utils.py").is_file():
        print("Source code not found.")
        exit(1)


def build_executable(pack_into_zip: bool = False):
    base_path = Path(__file__).parent
    if (pyi_exe := shutil.which("pyinstaller")) is None:
        print("PyInstaller was not installed.")
        exit(1)
    command = [
        pyi_exe,
        "-D",
        base_path / "mystery" / "__main__.py",
        "-n",
        "mystery",
        "--additional-hooks-dir",
        base_path,
        "--noconfirm",
        "--clean",
    ]
    if sys.platform in ["darwin", "win32"]:
        command.extend(["-w"])
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"PyInstaller returned non-zero exit status {result.returncode}.")
        exit(1)
    if pack_into_zip:
        mystery_ver = get_version()
        archive_name = "mystery-{}_{}_{}_py{}".format(
            mystery_ver,
            platform.system(),
            platform.machine(),
            platform.python_version(),
        )
        shutil.make_archive(archive_name, "zip", base_path / "dist" / "mystery")
        shutil.rmtree(Path.cwd() / "dist", ignore_errors=True)
    os.remove(Path.cwd() / "mystery.spec")
    shutil.rmtree(Path.cwd() / "build", ignore_errors=True)


def build_pyz(compressed: bool = False):
    base_path = Path(__file__).parent
    shutil.copytree(
        base_path / "mystery",
        base_path / "build" / "mystery",
        ignore=shutil.ignore_patterns("*.pyc", "__pycache__"),
        dirs_exist_ok=True,
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            base_path / "requirements.txt",
            "--target",
            base_path / "build",
        ],
        check=False,
    )
    if result.returncode != 0:
        print(f"pip returned non-zero exit status {result.returncode}.")
        exit(1)
    zipapp.create_archive(
        base_path / "build",
        base_path / "mystery.pyz",
        interpreter="/usr/bin/env python3",
        main="mystery.__main__:start",
        compressed=compressed,
    )
    shutil.rmtree(base_path / "build", ignore_errors=True)


if __name__ == "__main__":
    args = parser.parse_args()
    check()
    if args.type == "exec":
        build_executable(pack_into_zip=args.pack)
    else:
        build_pyz(compressed=args.compressed)
